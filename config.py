import os
from dotenv import load_dotenv

load_dotenv()


# ===== Ollama =====
OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    #"mollysama/rwkv-7-g1d:1.5b"
    #"rwkv-7-g1c-nt"
    #"qwen3:0.6b"
    "phi3:mini"
)

OLLAMA_API_URL = os.getenv(
    "OLLAMA_API_URL",
    "http://127.0.0.1:11434/api/generate"
)

CALL_TIMEOUT = int(os.getenv(
    "CALL_TIMEOUT",
    "60"
))


# ===== Server =====
SERVER_HOST = os.getenv(
    "SERVER_HOST",
    "0.0.0.0"
)

SERVER_PORT = int(os.getenv(
    "SERVER_PORT",
    "8501"
))


# ===== Spam classify =====
MAX_TEXT_LEN = int(os.getenv(
    "MAX_TEXT_LEN",
    "1200"
))
