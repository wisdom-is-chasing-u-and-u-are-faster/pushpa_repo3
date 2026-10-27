import os
import sqlite3
from pathlib import Path


def get_db_path():
    db_url = os.getenv("DATABASE_URL", "sqlite:///./sports_management.db")
    db_path = "sports_management.db"
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
    return db_path


def get_db_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(force_reset=False):
    db_path = get_db_path()
    if force_reset and os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()

    # Run Schema
    schema_path = Path("db/schema.sql")
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    # Run Seeds
    seed_path = Path("db/seed.sql")
    if seed_path.exists():
        with open(seed_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
