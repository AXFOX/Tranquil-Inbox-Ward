# ollama_client.py
from typing import TypedDict, Any, List
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

def ollama_generate_logprobs(prompt: str) -> OllamaResponse:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "top_p": 1,
            "num_predict": 1,
            "logprobs": 3
        }
    }

    resp = requests.post(
        OLLAMA_API_URL,
        json=payload,
        timeout=CALL_TIMEOUT
    )
    resp.raise_for_status()
    return resp.json()
