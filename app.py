from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from spam_check import check_spam
from config import SERVER_HOST, SERVER_PORT


# ===== 请求模型（必须在路由之前） =====
class SpamCheckRequest(BaseModel):
    text: str


class Instance(BaseModel):
    token: List[str]


class TFServingRequest(BaseModel):
    instances: List[Instance]


# ===== FastAPI 初始化 =====
app = FastAPI(
    title="Tranquil Inbox Ward",
    description="Spam classification service based on Ollama logprobs",
    version="1.0.0",
)


# ===== 兼容 TF Serving 接口 =====
@app.post("/v1/models/emotion_model:predict")
def predict_tf_serving(req: TFServingRequest):
    if not req.instances:
        raise HTTPException(status_code=400, detail="No instances provided")

    instance = req.instances[0]

    if not instance.token or not instance.token[0].strip():
        raise HTTPException(status_code=400, detail="Empty token")

    text = instance.token[0].strip()

    try:
        return check_spam(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spam check failed: {e}")


# ===== 健康检查 =====
@app.get("/health")
def health():
    return {"status": "ok"}


# ===== 简单接口 =====
@app.post("/predict")
def predict(req: SpamCheckRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    try:
        return check_spam(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Spam check failed: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=SERVER_HOST, port=SERVER_PORT)
