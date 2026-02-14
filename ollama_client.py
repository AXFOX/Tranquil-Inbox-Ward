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
    logprobs: List[dict]  # 每个 token 的 logprob 信息

def ollama_generate_logprobs(prompt: str) -> OllamaResponse:
    """
    调用 Ollama API，返回完整 JSON，包括 logprobs
    """
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "logprobs": True,       # 获取每个 token 的 logprob
        "top_logprobs": 3,      # Ollama 返回每个 token 的前 3 个候选 logprobs
        "options": {
            "temperature": 0,
            "top_p": 1,
            "num_predict": 1
        }
    }

    resp = requests.post(
        OLLAMA_API_URL,
        json=payload,
        timeout=CALL_TIMEOUT
    )
    resp.raise_for_status()
    data = resp.json()

    # 确保 logprobs 字段存在
    if "logprobs" not in data or not isinstance(data["logprobs"], list):
        data["logprobs"] = []

    # 保证每个 token 的 top_logprobs 字段存在
    for token_info in data["logprobs"]:
        if "top_logprobs" not in token_info or not isinstance(token_info["top_logprobs"], list):
            token_info["top_logprobs"] = []

    return data
