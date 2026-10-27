import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from app.db.init_db import get_db_connection
from app.services.bracket_generator import generate_bracket

router = APIRouter(prefix="/api/v1/tournaments", tags=["Tournaments"])


class TournamentCreate(BaseModel):
    name: str
    sport: str = "Basketball"
    format: str = "single_elimination"
    start_date: str = "2026-11-01"
    end_date: str = "2026-11-15"


@router.get("")
def list_tournaments():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tournaments")
    rows = c.fetchall()
    conn.close()
    return {"tournaments": [dict(r) for r in rows]}


@router.post("", status_code=201)
def create_tournament(payload: TournamentCreate):
    tourn_id = f"tourn_{uuid.uuid4().hex[:6]}"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO tournaments (id, tenant_id, name, sport, format, status, start_date, end_date)
           VALUES (?, 't_default', ?, ?, ?, 'draft', ?, ?)""",
        (tourn_id, payload.name, payload.sport, payload.format, payload.start_date, payload.end_date)
    )
    conn.commit()
    conn.close()
    return {"id": tourn_id, "name": payload.name, "format": payload.format, "status": "draft"}


@router.post("/{tourn_id}/generate-bracket")
def get_or_generate_bracket(tourn_id: str, payload: dict = {}):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM teams WHERE tenant_id = 't_default'")
    teams = [dict(r) for r in c.fetchall()]
    conn.close()

    fmt = payload.get("format", "single_elimination")
    rounds = generate_bracket(teams, format_type=fmt)
    return {"tournament_id": tourn_id, "format": fmt, "rounds": rounds}


@router.get("/{tourn_id}/standings")
def get_standings(tourn_id: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM standings WHERE tournament_id = ? ORDER BY points DESC, point_diff DESC", (tourn_id,))
    rows = c.fetchall()
    conn.close()
    return {"tournament_id": tourn_id, "standings": [dict(r) for r in rows]}
