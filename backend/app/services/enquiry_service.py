from sqlalchemy.orm import Session

from app.models.enquiry import Enquiry
from app.schemas import EnquiryCreate


def create_enquiry(db: Session, data: EnquiryCreate) -> Enquiry:
    enquiry = Enquiry(product_name=data.product_name)
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry
