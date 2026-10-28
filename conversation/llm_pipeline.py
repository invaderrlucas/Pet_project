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
MODEL = "gemma:2b"

def sendMessage(message,local):
    if local == True:
        payload["model"] = MODEL
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
def ollama_start(timeout=30):
    if not ollama_running():
        print("Starting Ollama...")
        # start the server in the background, don't wait for it to exit
        subprocess.Popen(["ollama", "serve"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.time() + timeout
        while not ollama_running():
            if time.time() > deadline:
                raise RuntimeError("Ollama server did not come up")
            time.sleep(0.5)
    # preload the model and keep it in memory (empty prompt = just load)
    requests.post(f"{OLLAMA_URL}/api/generate",
                  json={"model": MODEL, "keep_alive": -1}, timeout=300)
    print("Ollama ready")
    