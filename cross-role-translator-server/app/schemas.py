from typing import List, Literal, Optional
from pydantic import BaseModel, Field


RoleType = Literal[
    "product_manager",
    "developer",
    "designer",
    "operator",
    "executive",
]


class InfoCompletionItem(BaseModel):
    item: str
    status: Literal["待确认", "已推断"]
    suggested_value: str = ""


class TranslateRequest(BaseModel):
    source_role: RoleType = Field(..., description="源角色")
    target_role: RoleType = Field(..., description="目标角色")
    content: str = Field(..., description="原始内容")


class TranslateResponse(BaseModel):
    detected_scene: str
    translated_message: str
    info_completion: List[InfoCompletionItem]
    risk_alerts: List[str]
    suggestion_for_source: str