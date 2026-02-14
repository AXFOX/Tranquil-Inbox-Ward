# classifier.py
import math

LABELS = ["A", "B", "C"]  # 顺序固定: A=正常, B=广告, C=诈骗

def softmax(logits):
    """标准 softmax"""
    m = max(logits)
    exps = [math.exp(x - m) for x in logits]
    s = sum(exps)
    return [e / s for e in exps]

def extract_probs_from_logprobs(ollama_json: dict):
    """
    将 Ollama logprobs 转换为 [normal, ad, scam] 概率
    对缺失 token 采用 -5 处理，而不是 -100
    """
    try:
        # 取第一个 token 的 top_logprobs
        top_logprobs_list = ollama_json["logprobs"][0]["top_logprobs"]
        top_logprobs_dict = {item["token"]: item["logprob"] for item in top_logprobs_list}
    except (KeyError, IndexError, TypeError):
        return [1/3, 1/3, 1/3]

    # 对 A/B/C token 做 softmax
    logits = []
    for label in LABELS:
        logits.append(top_logprobs_dict.get(label, -5))  # 缺失 token 设为 -5

    return softmax(logits)

def classify_from_ollama(ollama_json: dict):
    """
    优先软分类，异常或 logprobs 不完整时用硬分类兜底
    """
    probs = extract_probs_from_logprobs(ollama_json)

    # 如果返回均等概率（-兜底）或异常
    if probs == [1/3, 1/3, 1/3]:
        resp = ollama_json.get("response", "").strip().upper()
        if resp == "A":
            return [1.0, 0.0, 0.0]
        elif resp == "B":
            return [0.0, 1.0, 0.0]
        elif resp == "C":
            return [0.0, 0.0, 1.0]

    return probs
