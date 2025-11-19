from course_app.db.models import Exam
from course_app.db.schema import ExamSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, APIRouter

exam_router = APIRouter(prefix='/exam', tags=['Exams'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@exam_router.post('/', response_model=ExamSchema)
async def store_create(exam: ExamSchema, db: Session = Depends(get_db)):
    exam_db = Exam(**exam.dict())
    db.add(exam_db)
    db.commit()
    db.refresh(exam_db)
    return exam_db


@exam_router.get('/', response_model=List[ExamSchema])
async def exam_list(db: Session = Depends(get_db)):
    return db.query(Exam).all()


@exam_router.get('/{exam_id}/', response_model=ExamSchema)
async def exam_detail(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()

    if exam is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return exam


@exam_router.put('/{exam_id}/', response_model=ExamSchema)
async def exam_update(exam_id: int, exam: ExamSchema, db: Session = Depends(get_db)):
    exam_db = db.query(Exam).filter(Exam.id == exam_id).first()

    if exam_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for exam_key, exam_value in exam.dict().items():
        setattr(exam_db, exam_key, exam_value)

    db.commit()
    db.refresh(exam_db)
    return exam_db


@exam_router.delete('/{exam_id}/')
async def exam_delete(exam_id: int, db: Session = Depends(get_db)):
    exam_db = db.query(Exam).filter(Exam.id == exam_id).first()

    if exam_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(exam_db)
    db.commit()
    return {'message': 'This exam is deleted'}
