from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_static_html_pages_served():
    # Root index
    res_root = client.get("/")
    assert res_root.status_code == 200

    # Pages
    for page in ["dashboard.html", "team-management.html", "scorekeeper-pwa.html",
                 "fan-view.html", "registration.html", "tournament-wizard.html", "user-admin.html"]:
        res = client.get(f"/pages/{page}")
        assert res.status_code == 200, f"Failed to serve /pages/{page}"
