from sqlalchemy.orm import Session

from app.models.product import Product


def list_products(db: Session, category: str | None = None) -> list[Product]:
    query = db.query(Product)
    if category and category != "all":
        query = query.filter(Product.category == category)
    return query.all()
