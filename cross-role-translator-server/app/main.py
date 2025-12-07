from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import TranslateRequest, TranslateResponse
from .graph import run_translation

app = FastAPI(title="Cross Role Translator API")

# 简单 CORS 设置：方便本地 Vue 前端调试
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境记得收紧
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    return run_translation(req)
