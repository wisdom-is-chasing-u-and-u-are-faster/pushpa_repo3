from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_app_startup_and_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
