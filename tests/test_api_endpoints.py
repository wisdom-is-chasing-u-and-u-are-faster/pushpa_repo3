from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_dashboard_stats():
    res = client.get("/api/v1/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["active_tournaments"] >= 1
    assert data["new_registrations"] >= 1
    assert "recent_tournaments" in data
    assert "live_matches" in data


def test_tournaments_api():
    res = client.get("/api/v1/tournaments")
    assert res.status_code == 200
    assert len(res.json()["tournaments"]) >= 1

    create_payload = {
        "name": "Fall Invitational 2026",
        "sport": "Basketball",
        "format": "single_elimination",
        "start_date": "2026-11-20",
        "end_date": "2026-11-25"
    }
    create_res = client.post("/api/v1/tournaments", json=create_payload)
    assert create_res.status_code == 201
    assert create_res.json()["name"] == "Fall Invitational 2026"


def test_teams_and_roster_api():
    res = client.get("/api/v1/teams")
    assert res.status_code == 200
    teams = res.json()["teams"]
    assert len(teams) >= 1
    team_id = teams[0]["id"]

    roster_res = client.get(f"/api/v1/teams/{team_id}/roster")
    assert roster_res.status_code == 200
    assert "athletes" in roster_res.json()

    add_payload = {
        "name": "Alex Rivera",
        "jersey_number": 15,
        "position": "Forward",
        "dob": "2012-09-10",
        "waiver_signed": True,
        "coppa_consent": True,
        "guardian_email": "parent@example.com"
    }
    add_res = client.post(f"/api/v1/teams/{team_id}/roster", json=add_payload)
    assert add_res.status_code == 201
    assert add_res.json()["eligible"] is True


def test_admin_api():
    tenants_res = client.get("/api/v1/admin/tenants")
    assert tenants_res.status_code == 200
    assert len(tenants_res.json()["tenants"]) >= 1

    users_res = client.get("/api/v1/admin/users")
    assert users_res.status_code == 200
    assert len(users_res.json()["users"]) >= 1

    audit_res = client.get("/api/v1/admin/audit-logs")
    assert audit_res.status_code == 200
    assert len(audit_res.json()["logs"]) >= 1
