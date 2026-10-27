from app.db.init_db import init_database, get_db_connection


def test_init_database():
    init_database()
    conn = get_db_connection()
    c = conn.cursor()

    # Check tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {r[0] for r in c.fetchall()}
    assert "tenants" in tables
    assert "users" in tables
    assert "tournaments" in tables
    assert "teams" in tables
    assert "athletes" in tables
    assert "matches" in tables
    assert "match_events" in tables
    assert "standings" in tables
    assert "audit_logs" in tables

    # Check seeded tournament
    c.execute("SELECT COUNT(*) FROM tournaments")
    assert c.fetchone()[0] >= 1

    conn.close()
