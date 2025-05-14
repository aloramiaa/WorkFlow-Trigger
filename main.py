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

RENDER_URL = os.environ.get("RENDER_URL")  # Add your Render app's URL here

def trigger_workflow():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": REF}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 204:
        print("✅ GitHub workflow triggered.")
    else:
        print(f"❌ Failed to trigger: {response.status_code} - {response.text}")

def background_loop():
    while True:
        try:
            trigger_workflow()
            if RENDER_URL:
                ping_url = f"{RENDER_URL}/ping"
                r = requests.get(ping_url)
                print(f"🔄 Self-ping status: {r.status_code}")
        except Exception as e:
            print(f"Error in loop: {e}")
        time.sleep(600)  # 600 minutes

@app.route('/')
def home():
    return "🚀 Bot is running."

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    threading.Thread(target=background_loop).start()
    app.run(host="0.0.0.0", port=10000)
