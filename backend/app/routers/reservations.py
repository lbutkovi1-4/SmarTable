from datetime import timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/reservations", tags=["Rezervacije"])


def _overlap_filter(db: Session, table_id: int, start, end, exclude_id: Optional[int] = None):
    query = db.query(models.Reservation).filter(
        models.Reservation.table_id == table_id,
        models.Reservation.status != models.ReservationStatus.cancelled,
    )
    if exclude_id:
        query = query.filter(models.Reservation.id != exclude_id)

    conflicts = []
    for res in query.all():
        existing_start = res.reservation_date
        existing_end = res.reservation_date + timedelta(minutes=res.duration_minutes)
        if existing_start < end and existing_end > start:
            conflicts.append(res)
    return conflicts


@router.get("/availability", response_model=List[schemas.TableOut])
def check_availability(
    date: str = Query(...),
    duration_minutes: int = Query(90),
    guests_count: int = Query(1),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    from datetime import datetime
    start = datetime.fromisoformat(date)
    end = start + timedelta(minutes=duration_minutes)

    tables = db.query(models.RestaurantTable).filter(
        models.RestaurantTable.capacity >= guests_count
    ).all()

    available = []
    for table in tables:
        if not _overlap_filter(db, table.id, start, end):
            available.append(table)
    return available


@router.get("/", response_model=List[schemas.ReservationOut])
def list_reservations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Reservation)
    if current_user.role != models.UserRole.admin:
        query = query.filter(models.Reservation.user_id == current_user.id)
    return query.order_by(models.Reservation.reservation_date.desc()).all()


@router.post("/", response_model=schemas.ReservationOut, status_code=201)
def create_reservation(
    payload: schemas.ReservationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == payload.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Stol nije pronađen.")

    if payload.guests_count > table.capacity:
        raise HTTPException(status_code=400, detail=f"Stol ima kapacitet od {table.capacity} osoba.")

    start = payload.reservation_date
    end = start + timedelta(minutes=payload.duration_minutes)

    conflicts = _overlap_filter(db, table.id, start, end)
    if conflicts:
        raise HTTPException(status_code=409, detail="Stol je već rezerviran u traženom terminu.")

    reservation = models.Reservation(
        user_id=current_user.id,
        table_id=table.id,
        reservation_date=start,
        duration_minutes=payload.duration_minutes,
        guests_count=payload.guests_count,
        status=models.ReservationStatus.confirmed,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation


@router.delete("/{reservation_id}", status_code=204)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Rezervacija nije pronađena.")

    if current_user.role != models.UserRole.admin and reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Nemate pravo otkazati ovu rezervaciju.")

    reservation.status = models.ReservationStatus.cancelled
    db.commit()
    return None


@router.patch("/{reservation_id}/status", response_model=schemas.ReservationOut)
def update_status(
    reservation_id: int,
    payload: schemas.ReservationStatusUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin),
):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Rezervacija nije pronađena.")

    reservation.status = payload.status
    db.commit()
    db.refresh(reservation)
    return reservation