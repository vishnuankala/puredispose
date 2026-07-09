from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas import OrderCreate


def create_order(db: Session, order_data: OrderCreate) -> Order:
    order = Order(phone=order_data.phone, status="new")
    db.add(order)
    db.commit()
    db.refresh(order)

    # --- Future AI hook ---
    # e.g. trigger_ai_followup(order)  -> auto-draft a WhatsApp/SMS quote message
    # This is the natural place to call an AI/bot service, since it already
    # has the full business context (the new order) before returning.

    return order


def list_orders(db: Session, limit: int = 100) -> list[Order]:
    return db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
