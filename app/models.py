from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    admission_no: str = Field(index=True, unique=True)
    first_name: str
    last_name: str
    class_name: str = Field(index=True)
    section: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_contact: Optional[str] = None
    is_active: bool = True


class FeeSchedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    class_name: Optional[str] = Field(default=None, index=True)
    term: str = Field(index=True)
    academic_year: str = Field(index=True)
    amount: float
    due_date: date
    is_mandatory: bool = True


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    fee_schedule_id: int = Field(foreign_key="feeschedule.id", index=True)
    issue_date: date = Field(default_factory=date.today)
    due_date: date
    amount: float
    balance: float
    status: str = Field(default="unpaid", index=True)  # unpaid, partial, paid, overdue


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.id", index=True)
    amount: float
    method: str = Field(default="cash")  # cash, bank, card, mobile
    reference: Optional[str] = None
    paid_at: datetime = Field(default_factory=datetime.utcnow)