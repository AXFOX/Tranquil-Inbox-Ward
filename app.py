from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from spam_check import check_spam
from config import SERVER_HOST, SERVER_PORT


# ===== FastAPI 初始化 =====
app = FastAPI(
    title="Tranquil Inbox Ward",
    description="Spam classification service based on Ollama logprobs",
    version="1.0.0",
)


# ===== 请求模型 =====
class SpamCheckRequest(BaseModel):
    text: str


# ===== 健康检查 =====
@app.get("/health")
def health():
    return {"status": "ok"}


# ===== 核心接口 =====
@app.post("/predict")
def predict(req: SpamCheckRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    try:
        result = check_spam(text)
        return result
    except Exception as e:
        # 避免 Ollama 或解析异常直接炸服务
        raise HTTPException(
            status_code=500,
            detail=f"Spam check failed: {e}"
        )


# ===== 仅用于本地 python app.py 启动 =====
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False
    )
