import uuid
from fastapi import APIRouter
from app.db.init_db import get_db_connection
from app.services.eligibility_service import validate_athlete_eligibility

router = APIRouter(prefix="/api/v1/athletes", tags=["Athletes"])


@router.post("/register", status_code=201)
def register_athlete(payload: dict):
    elig = validate_athlete_eligibility(payload)
    ath_id = f"ath_{uuid.uuid4().hex[:6]}"
    reg_id = f"reg_{uuid.uuid4().hex[:8]}"

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO athletes (id, first_name, last_name, dob, guardian_name, guardian_email,
                          guardian_phone, coppa_consent, waiver_signed, eligible)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            ath_id, payload.get(
                "first_name", ""), payload.get(
                "last_name", ""), payload.get(
                "dob", "2012-01-01"), payload.get(
                    "guardian_name", ""), payload.get(
                        "guardian_email", ""), payload.get(
                            "guardian_phone", ""), int(
                                payload.get(
                                    "coppa_consent", True)), int(
                                        payload.get(
                                            "medical_waiver", True)), int(
                                                elig["eligible"]))
    )
    conn.commit()
    conn.close()

    return {
        "registration_id": reg_id,
        "athlete_id": ath_id,
        "eligible": elig["eligible"],
        "coppa_verified": elig["coppa_verified"],
        "checkout_url": f"/pages/registration.html?session_id={reg_id}&status=success"
    }
