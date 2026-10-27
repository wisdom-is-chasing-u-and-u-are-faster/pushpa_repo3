from app.services.bracket_generator import generate_bracket
from app.services.eligibility_service import validate_athlete_eligibility


def test_bracket_generation():
    teams = [
        {"id": "t1", "name": "Team 1"},
        {"id": "t2", "name": "Team 2"},
        {"id": "t3", "name": "Team 3"},
        {"id": "t4", "name": "Team 4"}
    ]

    # Single Elimination
    rounds_single = generate_bracket(teams, format_type="single_elimination")
    assert len(rounds_single) == 1
    assert len(rounds_single[0]["matches"]) == 2

    # Round Robin
    rounds_rr = generate_bracket(teams, format_type="round_robin")
    assert len(rounds_rr) == 1
    assert len(rounds_rr[0]["matches"]) == 6  # 4 choose 2 = 6 matches


def test_eligibility_and_coppa_validation():
    # Valid eligible athlete (13 years old)
    valid_ath = {
        "dob": "2013-05-15",
        "coppa_consent": True,
        "waiver_signed": True
    }
    res = validate_athlete_eligibility(valid_ath, min_age=12, max_age=14)
    assert res["eligible"] is True

    # Athlete under 13 without COPPA consent
    young_ath = {
        "dob": "2014-06-10",
        "coppa_consent": False,
        "waiver_signed": True
    }
    res_young = validate_athlete_eligibility(young_ath, min_age=12, max_age=14)
    assert res_young["eligible"] is False
    assert "COPPA" in res_young["message"]
