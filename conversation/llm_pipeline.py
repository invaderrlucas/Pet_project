import requests
import subprocess
import time
import json


payload = {
            "model": "qwen3.6",
            "prompt": "",
            "stream": False
          #  "tools": ["web_search"]
}
URL_out = "http://100.103.136.116:11434/api/generate"
URL = "http://localhost:11434/api/generate"
OLLAMA_URL = "http://localhost:11434"

def sendMessage(message,local):
    if local == True:
        payload["prompt"] += (" " + message + " ")
        response = requests.post(
        URL, 
        json=payload,
        )
        print(response.json()["response"])
        payload["prompt"] += ( " " + response.json()["response"] + " ")
        
 
    elif local == False :
        payload["prompt"] += (" " + message + " ")
        response = requests.post(
        URL_out, 
        json=payload,
        )    
        print(response.json()["response"])
        payload["prompt"] += ( " " + response.json()["response"] + " ")

def ollama_running():
    try:
        return requests.get(OLLAMA_URL, timeout=1).ok
    except requests.exceptions.RequestException:
        return False
def ollama_start():
    if not ollama_running():
        print("Starting Ollama...")
        subprocess.run(["ollama", "run", "gemma:2b", "--keepalive", "-1", ""])

    