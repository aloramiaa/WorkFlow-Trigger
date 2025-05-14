from flask import Flask
import threading
import time
import requests
import os

app = Flask(__name__)

# GitHub Workflow Config
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OWNER = "aloramiaa"
REPO = "Eu-FarmBot"
WORKFLOW_FILE = "farm.yml"
REF = "main"

def trigger_workflow():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": REF}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 204:
        print("✅ Workflow triggered")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

def background_loop():
    while True:
        trigger_workflow()
        time.sleep(300)  # 5 minutes

@app.route('/')
def home():
    return "GitHub Workflow Trigger is running every 5 minutes."

if __name__ == '__main__':
    threading.Thread(target=background_loop).start()
    app.run(host="0.0.0.0", port=10000)
