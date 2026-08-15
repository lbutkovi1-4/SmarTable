from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, auth
from ..database import get_db

router = APIRouter(prefix="/api/tables", tags=["Stolovi"])


@router.get("/", response_model=List[schemas.TableOut])
def list_tables(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.RestaurantTable).all()


@router.post("/", response_model=schemas.TableOut, status_code=201)
def create_table(
    payload: schemas.TableCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin),
):
    table = models.RestaurantTable(**payload.model_dump())
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.put("/{table_id}", response_model=schemas.TableOut)
def update_table(
    table_id: int,
    payload: schemas.TableUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin),
):
    table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Stol nije pronađen.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(table, field, value)

    db.commit()
    db.refresh(table)
    return table


@router.delete("/{table_id}", status_code=204)
def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(auth.require_admin),
):
    table = db.query(models.RestaurantTable).filter(models.RestaurantTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Stol nije pronađen.")
    db.delete(table)
    db.commit()
    return None