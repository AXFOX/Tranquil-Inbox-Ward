# classifier.py
import math
from typing import List, Optional
from ollama_client import OllamaResponse


LABELS = ["A", "B", "C"]  # 顺序固定: A=正常, B=广告, C=诈骗

def softmax(logits: List[float]) -> List[float]:
    """标准 softmax"""
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps)
    return [e / s for e in exps]

def extract_probs_from_logprobs(ollama_json: OllamaResponse) -> Optional[List[float]]:
    """
    将 Ollama logprobs 转换为 [normal, ad, scam] 概率
    返回 None 表示 logprobs 不完整，需要硬分类兜底
    """
    try:
        logprobs = ollama_json.get("logprobs", [])
        if not logprobs:
            return None
        
        top_logprobs_list = logprobs[0].get("top_logprobs", [])
        if not top_logprobs_list:
            return None
            
        top_logprobs_dict = {item["token"]: item["logprob"] for item in top_logprobs_list}
        
        # 检查 A/B/C 都存在
        if not all(label in top_logprobs_dict for label in LABELS):
            return None
            
        logits = [top_logprobs_dict[label] for label in LABELS]
        return softmax(logits)
        
    except (KeyError, IndexError, TypeError):
        return None

def classify_from_ollama(ollama_json: OllamaResponse) -> List[float]:
    """
    优先软分类，logprobs 不完整时用硬分类兜底
    """
    probs = extract_probs_from_logprobs(ollama_json)
    
    # 软分类成功
    if probs is not None:
        return probs
    
    # 硬分类兜底：从响应文本提取答案
    resp = ollama_json.get("response", "").strip().upper()
    if resp == "A":
        return [1.0, 0.0, 0.0]
    elif resp == "B":
        return [0.0, 1.0, 0.0]
    elif resp == "C":
        return [0.0, 0.0, 1.0]
    
    # 两种方法都失败，返回均等概率
    return [1/3, 1/3, 1/3]
