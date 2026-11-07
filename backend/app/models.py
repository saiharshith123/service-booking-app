from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Text, Index, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="customer", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    bookings: Mapped[list["Booking"]] = relationship(back_populates="customer")

class Slot(Base):
    __tablename__ = "slots"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(String(120), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(200), default="Main branch")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        # A cancelled booking releases its slot; only confirmed bookings are unique.
        Index("uq_active_booking_slot", "slot_id", unique=True,
              postgresql_where=text("status = 'confirmed'")),
        Index("ix_booking_customer_created", "customer_id", "created_at"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id", ondelete="RESTRICT"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="confirmed", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    customer: Mapped[User] = relationship(back_populates="bookings")
    slot: Mapped[Slot] = relationship(back_populates="bookings")
