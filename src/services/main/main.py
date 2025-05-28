from flask import Flask, request, jsonify, redirect
import requests

app = Flask(__name__)

SEARCH_SERVICE_URL = "http://search-service:5000"
RECOMMEND_SERVICE_URL = "http://recommend-service:5000"

@app.route("/search", methods=["POST"])
def proxy_search():
    return requests.post(f"{SEARCH_SERVICE_URL}/search", json=request.get_json()).json()

@app.route("/recommend", methods=["POST"])
def proxy_recommend():
    return requests.post(f"{RECOMMEND_SERVICE_URL}/recommend", json=request.get_json()).json()

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return redirect("/health")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
