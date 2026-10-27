from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/sync", tags=["Sync"])


@router.get("/status")
def get_sync_status():
    return {"status": "online", "indexeddb_supported": True, "server_time": "2026-10-27T12:00:00Z"}
