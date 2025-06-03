from flask import Flask, request, jsonify, redirect
import requests

app = Flask(__name__)

SEARCH_SERVICE_URL = "http://search-service:5000"
RECOMMEND_SERVICE_URL = "http://recommend-service:5000"

@app.route("/search", methods=["POST"])
@app.route("/search/<diet>", methods=["POST"])
def proxy_search(diet=None):
    path = "/search" if not diet else f"/search/{diet}"
    # Forward JSON body (not query params)
    resp = requests.post(f"{SEARCH_SERVICE_URL}{path}", json=request.get_json())
    return jsonify(resp.json()), resp.status_code


# Proxy recommend endpoint (POST)
@app.route("/recommend", methods=["POST"])
def proxy_recommend():
    resp = requests.post(f"{RECOMMEND_SERVICE_URL}/recommend", json=request.get_json())
    return jsonify(resp.json()), resp.status_code

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/")
def home():
    return redirect("/health")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
