import json
import os
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from volcenginesdkarkruntime import Ark


from .schemas import TranslateRequest, TranslateResponse, InfoCompletionItem
from .prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLE

load_dotenv()

DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY")
if not DOUBAO_API_KEY:
    raise RuntimeError("请在环境变量或 .env 中配置 OPENAI_API_KEY")

client = Ark(
    api_key=DOUBAO_API_KEY,
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    )


class TranslationState(TypedDict):
    """LangGraph 状态结构"""
    source_role: str
    target_role: str
    content: str
    result: Optional[Dict[str, Any]]  # 保存 LLM 输出结构


def _call_llm(source_role: str, target_role: str, content: str) -> Dict[str, Any]:
    """实际调用大模型，返回 dict"""
    user_message = (
        f"源角色: {source_role}\n"
        f"目标角色: {target_role}\n"
        "原始内容:\n"
        f"{content}\n\n"
        "请按照系统提示返回 JSON。"
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": FEW_SHOT_EXAMPLE},
        {"role": "user", "content": user_message},
    ]

    resp = client.chat.completions.create(
        model="doubao-seed-1-6-thinking-250715", 
        messages=messages,
        temperature=0.3,
    )

    raw = resp.choices[0].message.content or ""
    raw = raw.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].lstrip()

    try:
        data = json.loads(raw)
        return data
    except json.JSONDecodeError:
        # JSON 解析失败时再做一次修复调用
        repair_messages = [
            {
                "role": "system",
                "content": "你是一个 JSON 修复助手。请将用户提供的内容修复为合法 JSON，仅输出 JSON。"
            },
            {"role": "user", "content": raw},
        ]
        repair_resp = client.chat.completions.create(
            model="doubao-seed-1-6-thinking-250715",
            messages=repair_messages,
            temperature=0.0,
        )
        repaired = repair_resp.choices[0].message.content or ""
        repaired = repaired.strip()
        if repaired.startswith("```"):
            repaired = repaired.strip("`")
            if repaired.startswith("json"):
                repaired = repaired[4:].lstrip()
        return json.loads(repaired)


def translate_node(state: TranslationState) -> TranslationState:
    """LangGraph 节点：执行一次翻译"""
    result = _call_llm(
        source_role=state["source_role"],
        target_role=state["target_role"],
        content=state["content"],
    )
    state["result"] = result
    return state


# 构建 LangGraph 工作流
builder = StateGraph(TranslationState)
builder.add_node("translate", translate_node)
builder.add_edge(START, "translate")
builder.add_edge("translate", END)

translate_graph = builder.compile()


def run_translation(req: TranslateRequest) -> TranslateResponse:
    """提供给 FastAPI 调用的封装函数"""
    init_state: TranslationState = {
        "source_role": req.source_role,
        "target_role": req.target_role,
        "content": req.content,
        "result": None,
    }
    output_state = translate_graph.invoke(init_state)
    result = output_state["result"] or {}

    # 用 Pydantic 做一次“强校验”
    return TranslateResponse(
        detected_scene=result.get("detected_scene", "其他"),
        translated_message=result.get("translated_message", ""),
        info_completion=[
            InfoCompletionItem(
                item=item.get("item", ""),
                status=item.get("status", "待确认"),
                suggested_value=item.get("suggested_value", "") or "",
            )
            for item in result.get("info_completion", []) or []
        ],
        risk_alerts=result.get("risk_alerts", []) or [],
        suggestion_for_source=result.get("suggestion_for_source", ""),
    )