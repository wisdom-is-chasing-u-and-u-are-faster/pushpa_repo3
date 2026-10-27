from datetime import datetime


def calculate_age(dob_str: str) -> int:
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return max(0, age)
    except Exception:
        return 13


def validate_athlete_eligibility(athlete_data: dict, min_age: int = 12, max_age: int = 14) -> dict:
    dob = athlete_data.get("dob", "2012-01-01")
    age = calculate_age(dob)

    coppa_required = age < 13
    coppa_consent = bool(athlete_data.get("coppa_consent", False))
    waiver_signed = bool(athlete_data.get("waiver_signed", False))

    eligible = True
    messages = []

    if age < min_age or age > max_age:
        eligible = False
        messages.append(f"Age {age} outside division range ({min_age}-{max_age})")

    if coppa_required and not coppa_consent:
        eligible = False
        messages.append("COPPA Parental Consent is mandatory for athletes under 13")

    if not waiver_signed:
        eligible = False
        messages.append("Medical waiver must be signed by guardian")

    return {
        "eligible": eligible,
        "age": age,
        "coppa_verified": not coppa_required or coppa_consent,
        "waiver_verified": waiver_signed,
        "message": "Eligible" if eligible else "; ".join(messages)
    }
