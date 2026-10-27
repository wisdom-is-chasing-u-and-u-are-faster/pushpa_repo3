import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.init_db import init_database
from app.services.websocket_manager import ws_manager
from app.api.dashboard import router as dashboard_router
from app.api.tournaments import router as tournaments_router
from app.api.teams import router as teams_router
from app.api.matches import router as matches_router
from app.api.athletes import router as athletes_router
from app.api.payments import router as payments_router
from app.api.admin import router as admin_router
from app.api.sync import router as sync_router

app = FastAPI(title="Sports Management Application", version="1.0.0")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_database()


@app.get("/health")
def health_check():
    return {"status": "ok", "uptime": 100.0, "timestamp": "2026-10-27T12:00:00Z"}


@app.websocket("/ws/match/{match_id}")
async def websocket_match_endpoint(websocket: WebSocket, match_id: str):
    await ws_manager.connect(websocket, channel=f"match_{match_id}")
    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast_to_channel(f"match_{match_id}", data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, channel=f"match_{match_id}")

app.include_router(dashboard_router)
app.include_router(tournaments_router)
app.include_router(teams_router)
app.include_router(matches_router)
app.include_router(athletes_router)
app.include_router(payments_router)
app.include_router(admin_router)
app.include_router(sync_router)

if os.path.exists("public"):
    if os.path.exists("public/pages"):
        app.mount("/pages", StaticFiles(directory="public/pages"), name="pages")
    if os.path.exists("public/js"):
        app.mount("/js", StaticFiles(directory="public/js"), name="js")
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
