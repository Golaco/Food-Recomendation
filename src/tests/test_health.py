import requests

def test_recommend_health():
    r = requests.get("http://localhost:5000/health")
    assert r.status_code == 200