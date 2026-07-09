from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProductOut
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def get_products(category: str | None = Query(default=None), db: Session = Depends(get_db)):
    """Returns catalog items, optionally filtered by category (cups/plates/others)."""
    return product_service.list_products(db, category)
