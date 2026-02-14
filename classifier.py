# classifier.py
import math

LABELS = ["A", "B", "C"]  # 顺序必须固定：A=正常, B=广告, C=诈骗


def softmax(xs):
    """将 logits 转换为概率分布"""
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


def extract_probs_from_logprobs(ollama_json: dict):
    """
    返回 [normal, ad, scam] 概率
    """
    try:
        top_logprobs = ollama_json["logprobs"][0]["top_logprobs"][0]
    except (KeyError, IndexError, TypeError):
        return [1/3, 1/3, 1/3]

    logits = []
    for label in LABELS:
        # 如果 top_logprobs 没有这个 token，就给一个很小的 logit
        logits.append(top_logprobs.get(label, -100))

    return softmax(logits)



def classify_from_ollama(ollama_json: dict):
    """
    优先使用 logprobs 做软分类，如果不存在 logprobs 或非法输出，退回 hard 分类
    """
    # 先尝试软分类
    probs = extract_probs_from_logprobs(ollama_json)

    # 如果返回的都是相等概率（说明 logprobs 异常），使用硬分类兜底
    if probs == [1/3, 1/3, 1/3]:
        resp = ollama_json.get("response", "").strip().upper()
        if resp == "A":
            return [1.0, 0.0, 0.0]
        elif resp == "B":
            return [0.0, 1.0, 0.0]
        elif resp == "C":
            return [0.0, 0.0, 1.0]

    return probs
