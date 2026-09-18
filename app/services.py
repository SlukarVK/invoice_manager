from datetime import date


def calculate_vat(amount_without_vat: float, vat_rate:float):
    vat_amount = amount_without_vat * vat_rate / 100
    total_amount = vat_amount + amount_without_vat

    return vat_amount, total_amount

def get_invoice_status(due_date: date, current_status: str):
    if current_status == "UNPAID" and due_date < date.today():
        return "OVERDUE"

    return current_status