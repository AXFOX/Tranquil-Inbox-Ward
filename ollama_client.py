# ollama_client.py
from typing import TypedDict, List
import requests
from config import OLLAMA_API_URL, OLLAMA_MODEL, CALL_TIMEOUT

class OllamaResponse(TypedDict, total=False):
    model: str
    response: str
    done: bool
    done_reason: str
    context: List[int]
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    logprobs: list  # 新增，用于存放 token logprobs
    top_logprobs: list  # 新增，用于存放每个 token 的 top logprobs

def ollama_generate_logprobs(prompt: str) -> OllamaResponse:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,          # 注意 Python 布尔值首字母大写
        "logprobs": True,         # 顶级字段，确保返回 logprobs
        "top_logprobs": 3,        # 可选，返回每个 token 前 3 个概率
        "options": {
            "temperature": 0,
            "top_p": 1,
            "num_predict": 1       # 必须 >=1 才会生成 token 和 logprobs
        }
    }

    resp = requests.post(
        OLLAMA_API_URL,
        json=payload,
        timeout=CALL_TIMEOUT
    )
    resp.raise_for_status()
    return resp.json()
