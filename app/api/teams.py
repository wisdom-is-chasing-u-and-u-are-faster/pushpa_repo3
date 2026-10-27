import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from app.db.init_db import get_db_connection
from app.services.eligibility_service import validate_athlete_eligibility

router = APIRouter(prefix="/api/v1/teams", tags=["Teams"])


class TeamCreate(BaseModel):
    name: str
    division_id: str = "div_u14"
    coach_name: str = "Head Coach"


class AthleteAdd(BaseModel):
    name: str
    jersey_number: int = 1
    position: str = "Guard"
    dob: str = "2012-05-15"
    waiver_signed: bool = True
    coppa_consent: bool = True
    guardian_email: str = "guardian@example.com"


@router.get("")
def list_teams():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    rows = c.fetchall()
    conn.close()
    return {"teams": [dict(r) for r in rows]}


@router.post("", status_code=201)
def create_team(payload: TeamCreate):
    team_id = f"team_{uuid.uuid4().hex[:6]}"
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO teams (id, tenant_id, division_id, name, coach_name, eligibility_status)
           VALUES (?, 't_default', ?, ?, ?, 'eligible')""",
        (team_id, payload.division_id, payload.name, payload.coach_name)
    )
    conn.commit()
    conn.close()
    return {"id": team_id, "name": payload.name, "division_id": payload.division_id}


@router.get("/{team_id}/roster")
def get_team_roster(team_id: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM athletes WHERE team_id = ?", (team_id,))
    rows = c.fetchall()
    conn.close()
    return {"team_id": team_id, "athletes": [dict(r) for r in rows]}


@router.post("/{team_id}/roster", status_code=201)
def add_athlete_to_roster(team_id: str, payload: AthleteAdd):
    p_dict = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    eligibility = validate_athlete_eligibility(p_dict)
    ath_id = f"ath_{uuid.uuid4().hex[:6]}"
    names = payload.name.split(" ", 1)
    first_name = names[0]
    last_name = names[1] if len(names) > 1 else ""

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO athletes (id, team_id, first_name, last_name, jersey_number, position, dob,
                          guardian_email, coppa_consent, waiver_signed, eligible)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (ath_id, team_id, first_name, last_name, payload.jersey_number, payload.position, payload.dob,
         payload.guardian_email, int(payload.coppa_consent), int(payload.waiver_signed), int(eligibility["eligible"]))
    )
    conn.commit()
    conn.close()
    return {"athlete_id": ath_id, "eligible": eligibility["eligible"],
            "age": eligibility["age"], "validation_message": eligibility["message"]}
