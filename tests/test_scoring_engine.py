from app.services.scoring_engine import record_match_event


def test_score_increment_and_idempotency():
    match_id = "match_001"

    evt1 = {
        "idempotency_key": "scoring_test_unique_key_001",
        "event_type": "POINTS",
        "team": "home",
        "points": 3,
        "period": "Q3",
        "game_clock_seconds": 400
    }
    res1 = record_match_event(match_id, evt1)
    assert res1["home_score"] >= 45

    res_dup = record_match_event(match_id, evt1)
    assert res_dup["status"] == "duplicate_skipped"
