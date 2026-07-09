from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Order(Base):
    """A 'Get a Quote' request submitted from the contact form."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(10), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="new")  # new, contacted, closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
