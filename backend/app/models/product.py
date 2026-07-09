from sqlalchemy import Column, Integer, String, Float, Text

from app.database import Base


class Product(Base):
    """A catalog item, mirrors the product cards shown on the site."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(30), nullable=False, index=True)  # cups, plates, others
    description = Column(Text, nullable=True)
    price_per_piece = Column(Float, nullable=False)
    badge = Column(String(30), nullable=True)  # "Eco", "Popular", etc.
