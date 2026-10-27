from fastapi import APIRouter, HTTPException
from app.db.init_db import get_db_connection
from app.services.scoring_engine import record_match_event

router = APIRouter(prefix="/api/v1/matches", tags=["Matches"])


@router.get("/{match_id}")
def get_match_details(match_id: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Match not found")

    c.execute("SELECT * FROM match_events WHERE match_id = ? ORDER BY created_at DESC", (match_id,))
    events = [dict(e) for e in c.fetchall()]
    conn.close()

    m = dict(row)
    return {
        "match_id": m["id"],
        "tournament_name": "U14 Boys Championship",
        "home_team": {"id": m["home_team_id"], "name": m["home_team_name"],
                       "score": m["home_score"], "fouls": m["home_fouls"]},
        "away_team": {"id": m["away_team_id"], "name": m["away_team_name"],
                       "score": m["away_score"], "fouls": m["away_fouls"]},
        "period": m["period"],
        "game_clock_seconds": m["game_clock_seconds"],
        "status": m["status"],
        "events": events
    }


@router.post("/{match_id}/events", status_code=201)
def post_match_event(match_id: str, payload: dict):
    res = record_match_event(match_id, payload)
    return res


@router.post("/{match_id}/events/batch")
def sync_offline_events(match_id: str, payload: dict):
    events = payload.get("events", [])
    synced = 0
    dups = 0
    for evt in events:
        res = record_match_event(match_id, evt)
        if res.get("status") == "duplicate_skipped":
            dups += 1
        else:
            synced += 1
    return {"synced_count": synced, "duplicates_skipped": dups}
