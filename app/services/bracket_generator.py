import uuid


def generate_bracket(teams: list, format_type: str = "single_elimination") -> list:
    if not teams:
        return []

    rounds = []
    if format_type in ["single_elimination", "double_elimination"]:
                # Pad to power of 2 if necessary
        paired_teams = list(teams)

        matches = []
        for i in range(0, len(paired_teams), 2):
            home = paired_teams[i]
            away = paired_teams[i + 1] if i + 1 < len(paired_teams) else {"id": "bye", "name": "BYE"}
            matches.append({
                "match_id": f"m_{uuid.uuid4().hex[:6]}",
                "home_team_id": home.get("id"),
                "home_team_name": home.get("name"),
                "away_team_id": away.get("id"),
                "away_team_name": away.get("name"),
                "court": f"Court {(i//2)%4 + 1}",
                "scheduled_time": "10:00 AM",
                "status": "scheduled"
            })

        rounds.append({
            "round_number": 1,
            "name": "Quarterfinals" if len(matches) == 4 else ("Semifinals" if len(matches) == 2 else "Finals"),
            "matches": matches
        })
    elif format_type == "round_robin":
        matches = []
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                matches.append({
                    "match_id": f"m_{uuid.uuid4().hex[:6]}",
                    "home_team_id": teams[i]["id"],
                    "home_team_name": teams[i]["name"],
                    "away_team_id": teams[j]["id"],
                    "away_team_name": teams[j]["name"],
                    "court": f"Court {(len(matches)%3)+1}",
                    "scheduled_time": f"{10 + len(matches)}:00 AM",
                    "status": "scheduled"
                })
        rounds.append({
            "round_number": 1,
            "name": "Group Stage",
            "matches": matches
        })

    return rounds
