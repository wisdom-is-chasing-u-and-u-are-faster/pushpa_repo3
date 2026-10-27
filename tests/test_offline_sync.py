from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_batch_offline_events_sync():
    match_id = "match_001"
    batch_payload = {
        "events": [
            {
                "idempotency_key": "sync_evt_unique_101",
                "event_type": "POINTS",
                "team": "home",
                "points": 2,
                "game_clock_seconds": 350
            },
            {
                "idempotency_key": "sync_evt_unique_102",
                "event_type": "POINTS",
                "team": "away",
                "points": 3,
                "game_clock_seconds": 340
            }
        ]
    }
    res = client.post(f"/api/v1/matches/{match_id}/events/batch", json=batch_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["synced_count"] == 2
