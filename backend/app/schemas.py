from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class SlotCreate(BaseModel):
    service_name: str = Field(min_length=2, max_length=120)
    starts_at: datetime
    ends_at: datetime
    location: str = Field(default="Main branch", max_length=200)

    @model_validator(mode="after")
    def valid_range(self):
        if self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be later than starts_at")
        return self

class SlotOut(BaseModel):
    id: int
    service_name: str
    starts_at: datetime
    ends_at: datetime
    location: str
    is_active: bool
    available: bool = True
    model_config = ConfigDict(from_attributes=True)

class BookingCreate(BaseModel):
    slot_id: int
    notes: str | None = Field(default=None, max_length=1000)

class BookingReschedule(BaseModel):
    slot_id: int

class BookingOut(BaseModel):
    id: int
    customer_id: int
    slot_id: int
    status: str
    notes: str | None
    created_at: datetime
    slot: SlotOut
    customer: UserOut | None = None
    model_config = ConfigDict(from_attributes=True)
