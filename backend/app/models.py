from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Telemetry(Base):

    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    device_id: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True
    )

    temperature_c: Mapped[float] = mapped_column(
        Float
    )

    humidity_pct: Mapped[float] = mapped_column(
        Float
    )
