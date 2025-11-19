from course_app.db.models import Assignment
from course_app.db.schema import AssignmentSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional, List

assignment_router = APIRouter(prefix='/assignment', tags=['Assignments'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@assignment_router.post('/', response_model=AssignmentSchema)
async def create_assignment(assignment: AssignmentSchema, db: Session = Depends(get_db)):
    assignment_db = Assignment(**assignment.dict())
    db.add(assignment_db)
    db.commit()
    db.refresh(assignment_db)
    return assignment_db


@assignment_router.get('/', response_model=List[AssignmentSchema])
async def list_assignment(db: Session = Depends(get_db)):
    return db.query(Assignment).all()


@assignment_router.get('/{assignment_id}/', response_model=AssignmentSchema)
async def detail_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')
    return assignment


@assignment_router.put('/{assignment_id}/', response_model=AssignmentSchema)
async def update_assignment(assignment_id: int, assignment: AssignmentSchema, db: Session = Depends(get_db)):
    assignment_db = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment_db is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')

    for assignment_key, assignment_value in assignment.dict().items():
        setattr(assignment_db, assignment_key, assignment_value)

    db.commit()
    db.refresh(assignment_db)
    return assignment_db


@assignment_router.delete('/{assignment_id}/')
async def delete_category(assignment_id: int, db: Session = Depends(get_db)):
    assignment_db = db.query(Assignment).filter(Assignment.id == assignment_id).first()

    if assignment_db is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')

    db.delete(assignment_db)
    db.commit()
    return {'message': 'this assignment is deleted'}
