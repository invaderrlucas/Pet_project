import requests

URL = "http://192.168.0.104:11434/api/generate"
response = requests.post(
    URL, 
    json={
        "model": "qwen3.6",
        "prompt": "Why is the sky blue?",
        "stream": False,
    },
)
print(response.json()["response"])