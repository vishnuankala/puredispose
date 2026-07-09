from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EnquiryCreate, EnquiryOut
from app.services import enquiry_service

router = APIRouter(prefix="/api/enquiries", tags=["enquiries"])


@router.post("", response_model=EnquiryOut, status_code=201)
def submit_enquiry(enquiry: EnquiryCreate, db: Session = Depends(get_db)):
    """Called silently whenever a visitor clicks '+' on a product card."""
    return enquiry_service.create_enquiry(db, enquiry)
