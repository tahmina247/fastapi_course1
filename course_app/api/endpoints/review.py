from course_app.db.models import Review
from course_app.db.schema import ReviewSchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, APIRouter

review_router = APIRouter(prefix='/review', tags=['Reviews'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post('/', response_model=ReviewSchema)
async def review_create(review: ReviewSchema, db: Session = Depends(get_db)):
    review_db = Review(**review.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get('/', response_model=List[ReviewSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get('/{review_id}/', response_model=ReviewSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if review is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')
    return review


@review_router.put('/{review_id}/', response_model=ReviewSchema)
async def review_update(review_id: int, review: ReviewSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()

    if review_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    for review_key, review_value in review.dict().items():
        setattr(review_db, review_key, review_value)

    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.delete('/{review_id}/')
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()

    if review_db is None:
        raise HTTPException(status_code=400, detail='Мындай маалымат жок')

    db.delete(review_db)
    db.commit()
    return {'message': 'This store is deleted'}
