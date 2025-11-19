from course_app.db.models import Question
from course_app.db.schema import QuestionSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, APIRouter

question_router = APIRouter(prefix='/question', tags=['Questions'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@question_router.post('/', response_model=QuestionSchema)
async def question_create(question: QuestionSchema, db: Session = Depends(get_db)):
    question_db = Question(**question.dict())
    db.add(question_db)
    db.commit()
    db.refresh(question_db)
    return question_db


@question_router.get('/', response_model=List[QuestionSchema])
async def question_list(db: Session = Depends(get_db)):
    return db.query(Question).all()


@question_router.get('/{question_id}/', response_model=QuestionSchema)
async def exam_detail(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()

    if question is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return question


@question_router.put('/{question_id}/', response_model=QuestionSchema)
async def question_update(question_id: int, question: QuestionSchema, db: Session = Depends(get_db)):
    question_db = db.query(Question).filter(Question.id == question_id).first()

    if question_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for question_key, question_value in question.dict().items():
        setattr(question_db, question_key, question_value)

    db.commit()
    db.refresh(question_db)
    return question_db


@question_router.delete('/{question_id}/')
async def question_delete(question_id: int, db: Session = Depends(get_db)):
    question_db = db.query(Question).filter(Question.id == question_id).first()

    if question_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(question_db)
    db.commit()
    return {'message': 'This question is deleted'}
