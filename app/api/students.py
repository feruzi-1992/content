from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..core.db import get_session
from ..models import Student

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=Student, status_code=201)
async def create_student(student: Student, session: AsyncSession = Depends(get_session)) -> Student:
    existing = await session.exec(select(Student).where(Student.admission_no == student.admission_no))
    if existing.first():
        raise HTTPException(status_code=400, detail="Admission number already exists")
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student


@router.get("/", response_model=List[Student])
async def list_students(session: AsyncSession = Depends(get_session)) -> List[Student]:
    result = await session.exec(select(Student).order_by(Student.id))
    return result.all()


@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)) -> Student:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, data: Student, session: AsyncSession = Depends(get_session)) -> Student:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(student, k, v)
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return student


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)) -> None:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await session.delete(student)
    await session.commit()
    return None