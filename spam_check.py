# spam_check.py

from config import MAX_TEXT_LEN
from prompt import SPAM_CLASSIFY_PROMPT
from ollama_client import ollama_generate_logprobs
from classifier import classify_from_ollama

def _truncate_text(text: str) -> str:
    """超过 MAX_TEXT_LEN 截断"""
    if len(text) <= MAX_TEXT_LEN:
        return text
    return text[:MAX_TEXT_LEN]

def check_spam(text: str) -> dict:
    """
    核心函数：输入邮件文本，返回分类结果
    输出格式：
    {
        "predictions": [
            [normal_prob, ad_prob, scam_prob]
        ]
    }
    """
    text = text.strip()
    text = _truncate_text(text)
    
    prompt = SPAM_CLASSIFY_PROMPT.format(email=text)
    ollama_resp = ollama_generate_logprobs(prompt)
    
    probs = classify_from_ollama(ollama_resp)
    
    return {
        "predictions": [probs]  # [normal, ad, scam]
    }
