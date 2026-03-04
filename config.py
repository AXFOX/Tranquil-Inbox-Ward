import os
from dotenv import load_dotenv

load_dotenv()

# ===== Ollama =====
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mollysama/rwkv-7-g1d:1.5b-nothink")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434/api/generate")

# ===== Server =====
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8501"))

# ===== Spam classify =====
MAX_TEXT_LEN = int(os.getenv("MAX_TEXT_LEN", "2000"))
CALL_TIMEOUT = int(os.getenv("CALL_TIMEOUT", "60"))
