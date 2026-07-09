from datetime import datetime
from pydantic import BaseModel, Field, field_validator


# ---------- Orders ----------
class OrderCreate(BaseModel):
    phone: str = Field(..., description="10-digit Indian mobile number")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit() or len(v) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return v


class OrderOut(BaseModel):
    id: int
    phone: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Products ----------
class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    description: str | None
    price_per_piece: float
    badge: str | None

    class Config:
        from_attributes = True


# ---------- Enquiries ----------
class EnquiryCreate(BaseModel):
    product_name: str


class EnquiryOut(BaseModel):
    id: int
    product_name: str
    created_at: datetime

    class Config:
        from_attributes = True
