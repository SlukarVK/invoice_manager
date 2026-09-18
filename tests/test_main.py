from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Invoice Management API",
        "version": "1.0.0"
    }

def test_create_invoice(client):
    invoice_data = {
        "invoice_number": "2026-001",
        "supplier": "Test Supplier",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 10000,
        "vat_rate": 21
    }

    response = client.post("/invoices", json=invoice_data)

    assert response.status_code == 200

    data = response.json()

    assert data["invoice_number"] == "2026-001"
    assert data["supplier"] == "Test Supplier"
    assert data["amount_without_vat"] == 10000
    assert data["vat_rate"] == 21
    assert data["status"] == "UNPAID"

def test_get_invoices(client):
    invoice_data = {
        "invoice_number": "2026-002",
        "supplier": "ABC Company",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 5000,
        "vat_rate": 21
    }

    client.post("/invoices", json=invoice_data)

    response = client.get("/invoices")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["invoice_number"] == "2026-002"
    assert data[0]["supplier"] == "ABC Company"

def test_get_invoice(client):
    invoice_data = {
        "invoice_number": "2026-003",
        "supplier": "XYZ Company",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 7500,
        "vat_rate": 21
    }

    create_response = client.post("/invoices", json=invoice_data)

    assert create_response.status_code == 200

    invoice_id = create_response.json()["id"]

    response = client.get(f"/invoices/{invoice_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == invoice_id
    assert data["invoice_number"] == "2026-003"
    assert data["supplier"] == "XYZ Company"

def test_get_invoice_not_found(client):
    response = client.get("/invoices/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invoice not found"
    }

def test_update_invoice(client):
    invoice_data = {
        "invoice_number": "2026-004",
        "supplier": "Original Supplier",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 10000,
        "vat_rate": 21
    }

    create_response = client.post("/invoices", json=invoice_data)

    assert create_response.status_code == 200
    invoice_id = create_response.json()["id"]

    updated_data = {
        "invoice_number": "2026-004-UPDATED",
        "supplier": "New Supplier",
        "issue_date": "2026-08-20",
        "due_date": "2026-10-20",
        "amount_without_vat": 15000,
        "vat_rate": 21
    }

    response = client.put(f"/invoices/{invoice_id}", json=updated_data)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == invoice_id
    assert data["invoice_number"] == "2026-004-UPDATED"
    assert data["supplier"] == "New Supplier"
    assert data["amount_without_vat"] == 15000
    assert data["vat_rate"] == 21

def test_update_invoice_not_found(client):
    invoice_data = {
        "invoice_number": "2026-999",
        "supplier": "Test Supplier",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 1000,
        "vat_rate": 21
    }

    response = client.put(
        "/invoices/999",
        json=invoice_data
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invoice not found"
    }

def test_delete_invoice(client):
    invoice_data = {
        "invoice_number": "2026-005",
        "supplier": "Delete Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 5000,
        "vat_rate": 21
    }

    create_response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert create_response.status_code == 200

    invoice_id = create_response.json()["id"]

    response = client.delete(
        f"/invoices/{invoice_id}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Invoice deleted successfully"
    }

    get_response = client.get(
        f"/invoices/{invoice_id}"
    )

    assert get_response.status_code == 404

def test_delete_invoice_not_found(client):
    response = client.delete("/invoices/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invoice not found"
    }

def test_calculate_invoice(client):
    invoice_data = {
        "invoice_number": "2026-006",
        "supplier": "VAT Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 10000,
        "vat_rate": 21
    }

    create_response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert create_response.status_code == 200

    invoice_id = create_response.json()["id"]

    response = client.get(
        f"/invoices/{invoice_id}/calculation"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["invoice_id"] == invoice_id
    assert data["amount_without_vat"] == 10000
    assert data["vat_rate"] == 21
    assert data["vat_amount"] == 2100
    assert data["total_amount"] == 12100

def test_calculate_invoice_not_found(client):
    response = client.get("/invoices/999/calculation")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invoice not found"
    }
def test_create_invoice_invalid_amount(client):
    invoice_data = {
        "invoice_number": "2026-INVALID",
        "supplier": "Invalid Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 0,
        "vat_rate": 21
    }

    response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert response.status_code == 422

def test_create_invoice_negative_amount(client):
    invoice_data = {
        "invoice_number": "2026-INVALID-1",
        "supplier": "Invalid Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": -100,
        "vat_rate": 21
    }

    response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert response.status_code == 422


def test_create_invoice_vat_above_100(client):
    invoice_data = {
        "invoice_number": "2026-INVALID-2",
        "supplier": "Invalid Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 10000,
        "vat_rate": 101
    }

    response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert response.status_code == 422


def test_create_invoice_negative_vat(client):
    invoice_data = {
        "invoice_number": "2026-INVALID-3",
        "supplier": "Invalid Test",
        "issue_date": "2026-08-20",
        "due_date": "2026-09-20",
        "amount_without_vat": 10000,
        "vat_rate": -1
    }

    response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert response.status_code == 422

def test_create_invoice_invalid_dates(client):
    invoice_data = {
        "invoice_number": "2026-INVALID-DATE",
        "supplier": "Invalid Date Test",
        "issue_date": "2026-09-20",
        "due_date": "2026-08-20",
        "amount_without_vat": 10000,
        "vat_rate": 21
    }

    response = client.post(
        "/invoices",
        json=invoice_data
    )

    assert response.status_code == 422