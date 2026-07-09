from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import OrderCreate, OrderOut
from app.services import order_service

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=201)
def submit_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Called by the 'Get a Quote' form on the site."""
    return order_service.create_order(db, order)


@router.get("", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    """Admin-facing: list recent quote requests."""
    return order_service.list_orders(db)
