from fastapi import APIRouter
from app.db.init_db import get_db_connection

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/tenants")
def list_tenants():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tenants")
    rows = c.fetchall()
    conn.close()
    return {"tenants": [dict(r) for r in rows]}


@router.get("/users")
def list_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return {"users": [dict(r) for r in rows]}


@router.get("/audit-logs")
def list_audit_logs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM audit_logs ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return {"logs": [dict(r) for r in rows]}
