# classifier.py

import math

LABELS = ["A", "B", "C"]  # 顺序必须固定


def softmax(xs):
    m = max(xs)
    exps = [math.exp(x - m) for x in xs]
    s = sum(exps)
    return [e / s for e in exps]


def extract_probs_from_logprobs(ollama_json: dict):
    """
    返回 [normal, ad, scam] 概率
    """
    try:
        top_logprobs = ollama_json["logprobs"]["top_logprobs"][0]

    except (KeyError, IndexError):
        # 极端异常兜底
        return [1/3, 1/3, 1/3]
        
    logits = []
    for label in LABELS:
        logits.append(top_logprobs.get(label, -100))

    return softmax(logits)
# classifier.py

def hard_classify_from_response(resp: str):
    """
    将 Ollama 的 response 文本映射为分类概率
    A = 正常
    B = 广告
    C = 诈骗
    """
    if not resp:
        return [1/3, 1/3, 1/3]

    label = resp.strip().upper()

    if label == "A":
        return [1.0, 0.0, 0.0]
    elif label == "B":
        return [0.0, 1.0, 0.0]
    elif label == "C":
        return [0.0, 0.0, 1.0]

    # 非法输出兜底
    return [1/3, 1/3, 1/3]
