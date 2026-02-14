# spam_check.py
from config import MAX_TEXT_LEN
from prompt import SPAM_CLASSIFY_PROMPT
from ollama_client import ollama_generate_logprobs
from classifier import classify_from_ollama  # 使用软分类优先


def _truncate_text(text: str) -> str:
    """文本截断，防止 prompt 太长"""
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

    # 调用 Ollama API 获取 logprobs
    ollama_resp = ollama_generate_logprobs(prompt)

    print("OLLAMA RAW RESPONSE:", ollama_resp)  # 调试用，可删除

    # 使用 classify_from_ollama 做软分类，硬分类兜底
    probs = classify_from_ollama(ollama_resp)

    return {
        "predictions": [
            probs  # [normal, ad, scam]
        ]
    }
