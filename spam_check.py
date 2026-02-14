# spam_check.py

from config import MAX_TEXT_LEN
from prompt import SPAM_CLASSIFY_PROMPT
from ollama_client import ollama_generate_logprobs
#from classifier import extract_probs_from_logprobs
from classifier import hard_classify_from_response


def _truncate_text(text: str) -> str:
    if len(text) <= MAX_TEXT_LEN:
        return text
    return text[:MAX_TEXT_LEN]


def check_spam(text: str) -> dict:
    """
    核心函数：输入邮件文本，返回 spam_block 兼容结构
    """
    text = text.strip()
    text = _truncate_text(text)

    prompt = SPAM_CLASSIFY_PROMPT.format(email=text)

    ollama_resp = ollama_generate_logprobs(prompt)

    print("OLLAMA RAW RESPONSE:", ollama_resp)  # 调试用，正式环境可以删除

    # 安全取 response，显式类型收敛
    resp = ollama_resp.get("response")
    if not isinstance(resp, str):
        resp = ""

    #probs = extract_probs_from_logprobs(ollama_resp)
    probs = hard_classify_from_response(resp)

    return {
        "predictions": [
            probs  # [normal, ad, scam]
        ]
    }
