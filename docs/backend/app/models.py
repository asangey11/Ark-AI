from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DecalarativeBase, Mapped, mapped_column


class Base(DecalarativeBase):
    pass

class Target(Base):
    __tablename__ = "targets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    internal_url: Mapped[str] = mapped_column(String(100), nullable=False)

    application_type: Mapped[str] = mapped_column(String(100), nullable=False, default="web_application")

    vendor_label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Demo Vendor",
    )

    environment_label: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="sandbox",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_approved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Target id={self.id} name={self.name!r} approved={self.is_approved}>"


