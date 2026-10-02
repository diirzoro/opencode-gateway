from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import admin, auth, locations, profile
app = FastAPI(title="OpenCode Gateway API", version="0.1.0")
app.include_router(auth.router); app.include_router(profile.router); app.include_router(locations.router); app.include_router(admin.router)
@app.get("/api/health")
def health(): return {"status": "ok"}
frontend = Path(__file__).resolve().parents[2]
app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
