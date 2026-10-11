import requests
import json
payload = {
            "model": "qwen3.6",
            "prompt": "",
            "stream": False,
            "tools": ["web_search"]
}
URL_out = "http://100.103.136.116:11434/api/generate"
URL = "http://localhost:11434/api/generate"
def sendMessage(message,local):
    if local :
        payload["prompt"] += (" " + message + " ")
        response = requests.post(
        URL, 
        json=payload,
        )
    else :
        payload["prompt"] += (" " + message + " ")
        response = requests.post(
        URL_out, 
        json=payload,
        )

    print(response.json()["response"])
    payload["prompt"] += ( " " + response.json()["response"] + " ")
    