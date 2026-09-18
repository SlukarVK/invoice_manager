from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app import models
from app.schemas import InvoiceCreate, InvoiceResponse
from app.services import calculate_vat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice Management API",
    description="REST API for invoice management",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Invoice Management API",
        "version": "1.0.0"
    }

@app.post("/invoices")
def create_invoice(
        invoice: InvoiceCreate,
        db: Session = Depends(get_db)
):
    db_invoice = models.Invoice(
        invoice_number=invoice.invoice_number,
        supplier=invoice.supplier,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        amount_without_vat=invoice.amount_without_vat,
        vat_rate=invoice.vat_rate,
        status="UNPAID"
    )

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    return db_invoice

@app.get("/invoices", response_model=list[InvoiceResponse])
def get_invoices(db: Session = Depends(get_db)):
    invoices = db.query(models.Invoice).all()

    return invoices

@app.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found")

    return invoice

@app.put("/invoices/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
        invoice_id: int,
        invoice_data: InvoiceCreate,
        db: Session = Depends(get_db)
):
    invoice = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id
    ).first()
    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found")

    invoice.invoice_number = invoice_data.invoice_number
    invoice.supplier = invoice_data.supplier
    invoice.issue_date = invoice_data.issue_date
    invoice.due_date = invoice_data.due_date
    invoice.amount_without_vat = invoice_data.amount_without_vat
    invoice.vat_rate = invoice_data.vat_rate

    db.commit()
    db.refresh(invoice)

    return invoice


@app.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(
        models.Invoice.id == invoice_id
    ).first()

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found")

    db.delete(invoice)
    db.commit()

    return {"message": "Invoice deleted successfully"}

@app.get("/invoices/{invoice_id}/calculation")
def calculate_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found")

    vat_amount, total_amount = calculate_vat(
        invoice.amount_without_vat,
        invoice.vat_rate)

    return{
        "invoice_id": invoice_id,
        "amount_without_vat": invoice.amount_without_vat,
        "vat_rate": invoice.vat_rate,
        "vat_amount": vat_amount,
        "total_amount": total_amount
    }




