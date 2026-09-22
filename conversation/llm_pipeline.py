import requests
import json
payload = {
            "model": "qwen3.6",
            "prompt": "",
            "stream": False,
}
URL = "http://192.168.0.104:11434/api/generate"
def sendMessage(message):
    payload["prompt"] += (" " + message + " ")
    response = requests.post(
        URL, 
        json=payload,
    )
    print(response.json()["response"])