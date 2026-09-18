from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Invoice(Base):
    __tablename__ = "invoice"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False)
    supplier = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    amount_without_vat = Column(Float, nullable=False)
    vat_rate = Column(Float, nullable=False)
    status = Column(String, nullable=False, default= "UNPAID")
