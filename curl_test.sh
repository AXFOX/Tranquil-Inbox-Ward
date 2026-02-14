#curl test
#有效测试
curl http://localhost:11434/api/generate -d '{
  "model": "phi3:mini",
  "prompt": "请判断下面的邮件属于哪一类：A. 正常邮件B. 广告邮件C. 诈骗邮件 只输出一个大写字母，不要输出其他任何内容。邮件内容：您的账户存在异常，请点击链接进行验证",
  "logprobs": true,
   "stream": false
}'

## 待定测试
curl http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{
  "model": "mollysama/rwkv-7-g1c:1.5b",
  "prompt": "/set no_think 请判断下面的邮件属于哪一类：A. 正常邮件B. 广告邮件C. 诈骗邮件 只输出一个大写字母，不要输出其他任 何内容。邮件内容：t_Smtp.LocalIP",
  "stream": false,
  "logprobs": true,
  "top_logprobs": 1,
  "options": {
    "temperature": 0,
    "top_p": 1,
    "num_predict": 1024
    
  }
}'

curl -X POST http://127.0.0.1:8501/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"(&#39;Email delivered from&#39;, &#39;198.23.254.212&#39;, &#39;with port&#39;, 25)"}'
