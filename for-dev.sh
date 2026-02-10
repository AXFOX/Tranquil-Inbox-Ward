#!/usr/bin/env bash
#set -euo pipefail

# 可选参数：指定虚拟环境目录名（默认 .venv）
VENV_NAME="${1:-.TranquilInboxWard}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "工作目录: $ROOT_DIR"
if [ -d "$VENV_NAME" ]; then
    echo "虚拟环境 '$VENV_NAME' 已存在，使用该环境。"
else
    echo "创建虚拟环境 '$VENV_NAME'..."
    python3 -m venv "$VENV_NAME"
fi

echo "激活虚拟环境并安装依赖（在脚本内执行）..."
# shellcheck disable=SC1091
source "$VENV_NAME/bin/activate"

pip install --upgrade pip setuptools wheel

if [ -f "requirements.txt" ]; then
    echo "安装 requirements.txt 中的依赖..."
    pip install -r requirements.txt
else
    echo "未找到 requirements.txt，安装最小依赖 Flask..."
    pip install Flask
fi

# 检测 ollama 可用性（仅提醒，不安装）
if command -v ollama >/dev/null 2>&1; then
    OLLAMA_VER="$(ollama version 2>/dev/null || echo 'unknown')"
    echo "检测到 ollama: $OLLAMA_VER"
else
    echo "未检测到 ollama 命令。请参阅 README 安装 Ollama 并 pull 模型。"
fi

echo
echo "完成。要在当前 shell 中激活虚拟环境，运行："
echo "  source $VENV_NAME/bin/activate"