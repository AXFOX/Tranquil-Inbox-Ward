from flask import Flask, request, jsonify
import json
import urllib.request as urllib_request
import os
import logging
import re
import math
from dotenv import load_dotenv
from typing import Tuple

# ======================
# 环境 & 日志
# ======================

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("email_classifier")

# ======================
# 配置
# ======================

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mollysama/rwkv-7-g1c:1.5b")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434/api/generate")
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8501"))

MAX_TEXT_LEN = 1500  # 防止 prompt 过长

# ======================
# Flask
# ======================

app = Flask(__name__)

# ======================
# 分类器
# ======================

class EmailClassifier:
    """
    零训练邮件分类器：
    - LLM logits 作为主判别
    - 规则只做轻微 bias
    """

    PROMPT_TEMPLATE = """你是一个邮件分类系统。

请判断下面的邮件属于哪一类：
A. 正常邮件
B. 广告邮件
C. 诈骗邮件

示例：
邮件内容：双十一限时优惠，点击链接立刻领取优惠券。
答案：B

邮件内容：test smtp 198.23.254.212--
答案：B

邮件内容：smtp.linuxuser.site:25:0:127.0.0.1:1080:socks5:25
答案：B

邮件内容：gsudmswgebl iokijcsmg ykvhiy wocmydsmfa hsovovdq
答案：B

邮件内容：Have you received your funds valued $4,150,567.00 that was awarded to you by the NCIC.
答案：C

邮件内容：Your account has been compromised, please click the link to verify your information.
答案：C

邮件内容：会议时间调整为周三下午三点，请查收附件。
答案：A

邮件内容：项目进展已更新到文档，请大家查看。
答案：A

只输出一个大写字母，不要输出任何解释。

邮件内容：
{email}
"""

    SCAM_BIAS_PATTERN = re.compile(
        r"(点击|链接|验证码|转账|汇款|中奖|账户异常|verify|payment|transfer)",
        re.IGNORECASE
    )

    NORMAL_BIAS_PATTERN = re.compile(
        r"(smtp|imap|pop3|测试邮件|test mail|系统通知)",
        re.IGNORECASE
    )

    def _truncate(self, text: str) -> str:
        text = text.strip()
        return text[:MAX_TEXT_LEN] if len(text) > MAX_TEXT_LEN else text

    def _softmax(self, scores):
        max_v = max(scores)
        exps = [math.exp(s - max_v) for s in scores]
        total = sum(exps)
        return [v / total for v in exps]

    def call_llm_logits(self, text: str) -> Tuple[float, float, float]:
        """
        使用 Ollama /api/generate logprobs，直接取 A/B/C 的 logits
        """
        prompt = self.PROMPT_TEMPLATE.format(email=self._truncate(text))

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "top_p": 1,
                "num_predict": 1,
                "logprobs": 5
            }
        }

        try:
            req = urllib_request.Request(
                OLLAMA_API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            with urllib_request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            # /api/generate 返回 logprobs
            logprobs = result.get("logprobs", {})
            tokens = logprobs.get("tokens", [])
            token_logprobs = logprobs.get("token_logprobs", [])

            scores = {"A": -20.0, "B": -20.0, "C": -20.0}

            for tok, lp in zip(tokens, token_logprobs):
                t = tok.strip().upper()
                if t in scores:
                    scores[t] = lp

            probs = self._softmax([scores["A"], scores["B"], scores["C"]])
            return probs[0], probs[1], probs[2]

        except Exception as e:
            logger.error(f"LLM logits 调用失败: {e}")
            return 0.33, 0.33, 0.34

    def apply_rule_bias(
        self,
        probs: Tuple[float, float, float],
        text: str
    ) -> Tuple[float, float, float]:
        normal, ad, scam = probs

        if self.SCAM_BIAS_PATTERN.search(text):
            scam += 0.10

        if self.NORMAL_BIAS_PATTERN.search(text):
            normal += 0.10

        total = normal + ad + scam
        return normal / total, ad / total, scam / total

    def classify(self, text: str) -> Tuple[float, float, float]:
        if not text.strip():
            return 0.34, 0.33, 0.33

        probs = self.call_llm_logits(text)
        probs = self.apply_rule_bias(probs, text)
        return probs

classifier = EmailClassifier()

# ======================
# 接口
# ======================

@app.route("/health", methods=["GET"])
def health():
    try:
        tags_url = "http://127.0.0.1:11434/api/tags"
        req = urllib_request.Request(tags_url)
        with urllib_request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        models = [m.get("name", "") for m in data.get("models", [])]

        return jsonify({
            "status": "healthy",
            "ollama": "connected",
            "model_available": OLLAMA_MODEL in models,
            "available_models": models
        })

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


@app.route("/v1/models/emotion_model:predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "instances" not in data:
        return jsonify({"error": "Invalid request format"}), 400

    predictions = []

    for inst in data["instances"]:
        token = inst.get("token", [])
        text = " ".join(token) if isinstance(token, list) else str(token)

        normal, ad, scam = classifier.classify(text)
        predictions.append([normal, ad, scam])

        logger.info(f"预测: normal={normal:.3f}, ad={ad:.3f}, scam={scam:.3f}")

    return jsonify({"predictions": predictions})


@app.route("/classify", methods=["POST"])
def classify_direct():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    text = data["text"]
    normal, ad, scam = classifier.classify(text)

    label = max([("normal", normal), ("ad", ad), ("scam", scam)], key=lambda x: x[1])[0]

    return jsonify({
        "normal": normal,
        "ad": ad,
        "scam": scam,
        "prediction": label
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "Email Classification Service",
        "version": "3.1.1",
        "mode": "LLM logits (few-shot, /api/generate)",
        "model": OLLAMA_MODEL
    })


if __name__ == "__main__":
    logger.info(f"启动服务 {SERVER_HOST}:{SERVER_PORT}")
    logger.info(f"Ollama 模型: {OLLAMA_MODEL}")
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)
