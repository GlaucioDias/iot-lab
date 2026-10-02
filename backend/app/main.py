from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from sqlalchemy import desc

from .database import Base, SessionLocal, engine
from .models import Telemetry
from .mqtt_consumer import start_mqtt


app = FastAPI(
    title="IoT Telemetry Backend",
    version="1.0.0"
)


dashboard_path = (
    Path(__file__).parent.parent / "dashboard" / "index.html"
)


@app.on_event("startup")
def startup():

    Base.metadata.create_all(
        bind=engine
    )

    start_mqtt()


@app.get("/")
def dashboard():

    return FileResponse(
        dashboard_path
    )


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.get("/api/readings")
def readings(limit: int = 100):

    db = SessionLocal()

    try:

        rows = (
            db.query(Telemetry)
            .order_by(
                desc(Telemetry.timestamp)
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "device_id": row.device_id,
                "timestamp": row.timestamp.isoformat(),
                "temperature_c": row.temperature_c,
                "humidity_pct": row.humidity_pct
            }
            for row in reversed(rows)
        ]

    finally:

        db.close()
