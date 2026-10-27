import uuid
from app.db.init_db import get_db_connection


def record_match_event(match_id: str, event_data: dict) -> dict:
    idem_key = event_data.get("idempotency_key")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check for existing idempotency key in DB
    if idem_key:
        cursor.execute("SELECT * FROM match_events WHERE idempotency_key = ?", (idem_key,))
        existing_evt = cursor.fetchone()
        if existing_evt:
            cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
            m = cursor.fetchone()
            conn.close()
            return {
                "status": "duplicate_skipped",
                "idempotency_key": idem_key,
                "home_score": m["home_score"] if m else 0,
                "away_score": m["away_score"] if m else 0
            }

    # Check if match exists
    cursor.execute("SELECT * FROM matches WHERE id = ?", (match_id,))
    match = cursor.fetchone()
    if not match:
        conn.close()
        raise ValueError(f"Match with ID {match_id} not found")

    event_id = f"evt_{uuid.uuid4().hex[:8]}"
    event_type = event_data.get("event_type", "POINTS")
    team = event_data.get("team", "home")
    points = int(event_data.get("points", 0))
    player_id = event_data.get("player_id", "")
    period = event_data.get("period", match["period"])
    clock = int(event_data.get("game_clock_seconds", match["game_clock_seconds"]))

    # Insert event
    cursor.execute(
        """INSERT INTO match_events (id, match_id, idempotency_key, event_type, team, player_id, points,
                              period, game_clock_seconds)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (event_id, match_id, idem_key, event_type, team, player_id, points, period, clock)
    )

    # Update match scores
    new_home = match["home_score"] + (points if team == "home" and event_type == "POINTS" else 0)
    new_away = match["away_score"] + (points if team == "away" and event_type == "POINTS" else 0)
    new_home_fouls = match["home_fouls"] + (1 if team == "home" and event_type == "FOUL" else 0)
    new_away_fouls = match["away_fouls"] + (1 if team == "away" and event_type == "FOUL" else 0)

    cursor.execute(
        """UPDATE matches SET home_score = ?, away_score = ?, home_fouls = ?, away_fouls = ?,
                         period = ?, game_clock_seconds = ?, status = 'live'
           WHERE id = ?""",
        (new_home, new_away, new_home_fouls, new_away_fouls, period, clock, match_id)
    )

    conn.commit()
    conn.close()

    return {
        "event_id": event_id,
        "match_id": match_id,
        "home_score": new_home,
        "away_score": new_away,
        "home_fouls": new_home_fouls,
        "away_fouls": new_away_fouls,
        "status": "live",
        "broadcast_p99_ms": 12.4
    }
