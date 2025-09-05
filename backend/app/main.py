from fastapi import FastAPI
from sqlalchemy import text
import time

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="2-Host Starter API")

# TEMP: allow everything so preflight never fails
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # later you can lock this to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],          # includes OPTIONS
    allow_headers=["*"],
)

from .routers.health import router as health_router
from .routers.sites import router as sites_router
from .routers.devices import router as devices_router
from .routers.ipam import router as ipam_router
from .db import engine

app = FastAPI(title="2-Host Starter API")

# allow the Next.js app on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def wait_for_db(retries: int = 50, delay: float = 0.5):
    for i in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB reachable.")
            return
        except Exception as e:
            print(f"DB not ready ({i+1}/{retries}): {e}")
            time.sleep(delay)
    raise RuntimeError("Database did not become ready.")

@app.on_event("startup")
def on_startup():
    wait_for_db()

app.include_router(health_router)
app.include_router(sites_router)
app.include_router(devices_router)
app.include_router(ipam_router)
