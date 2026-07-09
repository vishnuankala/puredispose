from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Enquiry(Base):
    """Logged whenever a visitor clicks '+' on a product card."""
    __tablename__ = "enquiries"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
