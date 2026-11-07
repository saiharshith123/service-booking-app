from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Booking, Slot, User
from app.schemas import BookingCreate, BookingReschedule, BookingOut
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def get_available_slot(db, slot_id):
    slot = db.query(Slot).filter(Slot.id == slot_id, Slot.is_active.is_(True)).with_for_update().first()
    if not slot:
        raise HTTPException(404, "Active slot not found")
    if slot.starts_at <= datetime.now(timezone.utc):
        raise HTTPException(400, "Cannot book a past slot")
    occupied = db.query(Booking).filter(Booking.slot_id == slot_id, Booking.status == "confirmed").first()
    if occupied:
        raise HTTPException(409, "This slot is already booked")
    return slot

@router.post("", response_model=BookingOut, status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    slot = get_available_slot(db, data.slot_id)
    booking = Booking(customer_id=user.id, slot_id=slot.id, notes=data.notes, status="confirmed")
    db.add(booking)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "This slot was just booked by someone else")
    return db.query(Booking).options(joinedload(Booking.slot)).filter(Booking.id == booking.id).first()

@router.get("/mine", response_model=list[BookingOut])
def my_bookings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Booking).options(joinedload(Booking.slot)).filter(Booking.customer_id == user.id).order_by(Booking.created_at.desc()).all()

@router.patch("/{booking_id}/cancel", response_model=BookingOut)
def cancel_booking(booking_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = db.query(Booking).options(joinedload(Booking.slot)).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.customer_id != user.id and user.role != "admin":
        raise HTTPException(403, "You cannot cancel another user's booking")
    if booking.status != "confirmed":
        raise HTTPException(409, "Only confirmed bookings can be cancelled")
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking

@router.patch("/{booking_id}/reschedule", response_model=BookingOut)
def reschedule_booking(booking_id: int, data: BookingReschedule, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).with_for_update().first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.customer_id != user.id and user.role != "admin":
        raise HTTPException(403, "You cannot change another user's booking")
    if booking.status != "confirmed":
        raise HTTPException(409, "Only confirmed bookings can be rescheduled")
    get_available_slot(db, data.slot_id)
    booking.slot_id = data.slot_id
    db.commit()
    return db.query(Booking).options(joinedload(Booking.slot)).filter(Booking.id == booking_id).first()

@router.get("", response_model=list[BookingOut])
def all_bookings(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(Booking).options(joinedload(Booking.slot), joinedload(Booking.customer)).order_by(Booking.created_at.desc()).all()
