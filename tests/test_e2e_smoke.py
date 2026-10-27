from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_end_to_end_league_lifecycle():
    tourn_res = client.post("/api/v1/tournaments", json={
        "name": "E2E Championship 2026",
        "sport": "Basketball",
        "format": "single_elimination"
    })
    assert tourn_res.status_code == 201
    tourn_id = tourn_res.json()["id"]

    team_res = client.post("/api/v1/teams", json={
        "name": "E2E Champions",
        "coach_name": "Coach Steve"
    })
    assert team_res.status_code == 201
    team_id = team_res.json()["id"]

    ath_res = client.post(f"/api/v1/teams/{team_id}/roster", json={
        "name": "Michael Jordan Jr",
        "jersey_number": 23,
        "position": "Guard",
        "dob": "2012-02-17",
        "waiver_signed": True,
        "coppa_consent": True
    })
    assert ath_res.status_code == 201
    assert ath_res.json()["eligible"] is True

    bracket_res = client.post(f"/api/v1/tournaments/{tourn_id}/generate-bracket", json={
        "format": "single_elimination"
    })
    assert bracket_res.status_code == 200
    assert len(bracket_res.json()["rounds"]) >= 1

    score_res = client.post("/api/v1/matches/match_001/events", json={
        "idempotency_key": "e2e_evt_unique_999",
        "event_type": "POINTS",
        "team": "home",
        "points": 2,
        "game_clock_seconds": 600
    })
    assert score_res.status_code == 201
    assert score_res.json()["home_score"] > 0

    std_res = client.get(f"/api/v1/tournaments/{tourn_id}/standings")
    assert std_res.status_code == 200
