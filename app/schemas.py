from datetime import date
from pydantic import BaseModel, Field, model_validator, ConfigDict

class InvoiceCreate(BaseModel):
    invoice_number: str
    supplier: str
    issue_date: date
    due_date: date
    amount_without_vat: float = Field(gt=0)
    vat_rate: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.due_date < self.issue_date:
            raise ValueError("Due date cannot be before issue date")

        return self


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    supplier: str
    issue_date: date
    due_date: date
    amount_without_vat: float
    vat_rate: float
    status: str

    model_config = ConfigDict(from_attributes=True)
