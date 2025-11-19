from course_app.db.models import Category
from course_app.db.schema import CategorySchema
from course_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import Optional, List

category_router = APIRouter(prefix='/category', tags=['Categories'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/', response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    category_db = Category(category_name=category.category_name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.get('/', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.get('/{category_id}/', response_model=CategorySchema)
async def detail_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')
    return category


@category_router.put('/{category_id}/', response_model=CategorySchema)
async def update_category(category_id: int, category: CategorySchema, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()

    if category_db is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')

    category_db.category_name = category.category_name

    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete('/{category_id}/')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()

    if category_db is None:
        raise HTTPException(status_code=404, detail='Андай маалымат жок')

    db.delete(category_db)
    db.commit()
    return {'message': 'this category is deleted'}
