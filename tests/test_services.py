from datetime import date

from app.services import get_invoice_status


def test_overdue_invoice():
    status = get_invoice_status(
        date(2026, 8, 20),
        "UNPAID"
    )

    assert status == "OVERDUE"