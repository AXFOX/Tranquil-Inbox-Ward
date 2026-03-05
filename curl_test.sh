#!/bin/bash

# 测试 Ollama API 是否可用（使用当前配置的模型）
echo "=== 测试 Ollama API ==="
curl http://localhost:11434/api/generate -d '{
  "model": "mollysama/rwkv-7-g1d:1.5b-nothink",
  "prompt": "请判断下面的邮件属于哪一类：A. 正常邮件 B. 广告邮件 C. 诈骗邮件 只输出一个大写字母。邮件内容：您的账户存在异常，请点击链接进行验证",
  "logprobs": true,
  "top_logprobs": 3,
  "stream": false,
  "options": {
    "temperature": 0,
    "top_p": 1,
    "num_predict": 1
  }
}'

echo ""
echo "=== 测试服务 API (TF Serving 兼容) ==="
curl -X POST https://tranquil-inbox-ward.linuxuser.site/v1/models/emotion_model:predict\
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {"token": ["您的账户存在异常，请点击链接进行验证"]}
    ]
  }'

echo ""
echo "=== 健康检查 ==="
curl http://127.0.0.1:8501/health