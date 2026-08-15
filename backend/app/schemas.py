from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
from .models import UserRole, ReservationStatus


# ---------- USER ----------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    is_active: bool


class UserUpdateRole(BaseModel):
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- TABLE ----------
class TableCreate(BaseModel):
    name: str
    capacity: int
    description: Optional[str] = None


class TableUpdate(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None


class TableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    capacity: int
    description: Optional[str] = None


# ---------- RESERVATION ----------
class ReservationCreate(BaseModel):
    table_id: int
    reservation_date: datetime
    duration_minutes: int = 90
    guests_count: int


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    table_id: int
    reservation_date: datetime
    duration_minutes: int
    guests_count: int
    status: ReservationStatus
    table: TableOut
    user: UserOut


class ReservationStatusUpdate(BaseModel):
    status: ReservationStatus