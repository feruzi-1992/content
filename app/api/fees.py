from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.db import get_session
from ..models import FeeSchedule, Invoice, Payment, Student

router = APIRouter(prefix="/fees", tags=["fees"])


# Fee schedules
@router.post("/schedules", response_model=FeeSchedule, status_code=201)
async def create_fee_schedule(item: FeeSchedule, session: AsyncSession = Depends(get_session)) -> FeeSchedule:
    # Ensure due_date is a date instance (httpx/json may pass string)
    if isinstance(item.due_date, str):
        item.due_date = date.fromisoformat(item.due_date)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.get("/schedules", response_model=List[FeeSchedule])
async def list_fee_schedules(session: AsyncSession = Depends(get_session)) -> List[FeeSchedule]:
    result = await session.exec(select(FeeSchedule).order_by(FeeSchedule.due_date))
    return result.all()


# Invoice generation
@router.post("/invoices/generate/{student_id}", response_model=List[Invoice], status_code=201)
async def generate_invoices_for_student(
    student_id: int,
    term: str,
    academic_year: str,
    session: AsyncSession = Depends(get_session),
) -> List[Invoice]:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    schedules = await session.exec(
        select(FeeSchedule).where(
            FeeSchedule.term == term,
            FeeSchedule.academic_year == academic_year,
            (FeeSchedule.class_name == None) | (FeeSchedule.class_name == student.class_name),
        )
    )
    schedules_list = schedules.all()
    if not schedules_list:
        raise HTTPException(status_code=404, detail="No fee schedules found")

    created: List[Invoice] = []
    for schedule in schedules_list:
        exists = await session.exec(
            select(Invoice).where(
                Invoice.student_id == student.id,
                Invoice.fee_schedule_id == schedule.id,
            )
        )
        if exists.first():
            continue
        invoice = Invoice(
            student_id=student.id,
            fee_schedule_id=schedule.id,
            issue_date=date.today(),
            due_date=schedule.due_date,
            amount=schedule.amount,
            balance=schedule.amount,
            status="unpaid",
        )
        session.add(invoice)
        created.append(invoice)

    await session.commit()
    for inv in created:
        await session.refresh(inv)

    return created


@router.get("/invoices", response_model=List[Invoice])
async def list_invoices(session: AsyncSession = Depends(get_session)) -> List[Invoice]:
    result = await session.exec(select(Invoice).order_by(Invoice.due_date))
    return result.all()


# Payments
@router.post("/payments", response_model=Payment, status_code=201)
async def record_payment(payment: Payment, session: AsyncSession = Depends(get_session)) -> Payment:
    invoice = await session.get(Invoice, payment.invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    invoice.balance = max(0.0, invoice.balance - payment.amount)
    if invoice.balance == 0:
        invoice.status = "paid"
    elif invoice.balance < invoice.amount:
        invoice.status = "partial"

    session.add(payment)
    session.add(invoice)
    await session.commit()
    await session.refresh(payment)
    return payment