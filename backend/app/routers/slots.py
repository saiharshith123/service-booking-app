from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slot, Booking
from app.schemas import SlotCreate, SlotOut
from app.dependencies import require_admin

router = APIRouter(prefix="/slots", tags=["Slots"])

def serialize_slot(slot, db):
    booked = db.query(Booking).filter(Booking.slot_id == slot.id, Booking.status == "confirmed").first()
    return {**{c.name: getattr(slot, c.name) for c in slot.__table__.columns}, "available": slot.is_active and booked is None}

@router.get("", response_model=list[SlotOut])
def list_slots(db: Session = Depends(get_db), available_only: bool = Query(False)):
    slots = db.query(Slot).filter(Slot.is_active.is_(True), Slot.starts_at >= datetime.now(timezone.utc)).order_by(Slot.starts_at).all()
    result = [serialize_slot(s, db) for s in slots]
    return [s for s in result if s["available"]] if available_only else result

@router.post("", response_model=SlotOut, status_code=201)
def create_slot(data: SlotCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    if data.starts_at <= datetime.now(timezone.utc):
        raise HTTPException(400, "A slot must be in the future")
    slot = Slot(**data.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return serialize_slot(slot, db)

@router.patch("/{slot_id}/deactivate")
def deactivate_slot(slot_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    slot = db.get(Slot, slot_id)
    if not slot:
        raise HTTPException(404, "Slot not found")
    active_booking = db.query(Booking).filter(Booking.slot_id == slot_id, Booking.status == "confirmed").first()
    if active_booking:
        raise HTTPException(409, "Cancel or reschedule the booking before deactivating this slot")
    slot.is_active = False
    db.commit()
    return {"message": "Slot deactivated"}
