import asyncio
from datetime import date
import os

import pytest
from httpx import AsyncClient
from httpx import ASGITransport

from app.main import app
from app.core.db import init_db


@pytest.mark.asyncio
async def test_smoke_flow():
    # fresh DB file
    if os.path.exists("school_fees.db"):
        os.remove("school_fees.db")
    await init_db()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Trigger startup by hitting root
        r = await client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

        # Create student
        student_payload = {
            "admission_no": "ADM001",
            "first_name": "John",
            "last_name": "Doe",
            "class_name": "Grade 5",
        }
        r = await client.post("/students/", json=student_payload)
        assert r.status_code == 201, r.text
        student = r.json()

        # Create fee schedule
        schedule_payload = {
            "name": "Tuition",
            "class_name": "Grade 5",
            "term": "Term 1",
            "academic_year": "2025-2026",
            "amount": 500.0,
            "due_date": date.today().isoformat(),
            "is_mandatory": True,
        }
        r = await client.post("/fees/schedules", json=schedule_payload)
        assert r.status_code == 201, r.text

        # Generate invoice
        r = await client.post(
            f"/fees/invoices/generate/{student['id']}?term=Term+1&academic_year=2025-2026"
        )
        assert r.status_code == 201, r.text
        invoices = r.json()
        assert len(invoices) == 1
        invoice_id = invoices[0]["id"]
        assert invoices[0]["balance"] == 500.0

        # Pay partially
        payment_payload = {
            "invoice_id": invoice_id,
            "amount": 200.0,
            "method": "cash",
        }
        r = await client.post("/fees/payments", json=payment_payload)
        assert r.status_code == 201, r.text

        # Check invoices
        r = await client.get("/fees/invoices")
        assert r.status_code == 200
        inv = r.json()[0]
        assert inv["balance"] == 300.0
        assert inv["status"] == "partial"