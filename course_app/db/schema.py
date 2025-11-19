from pydantic import BaseModel
from typing import Optional
from course_app.db.models import RoleChoices, LevelChoices, ValidatorChoices, DifficultyLevelChoices, FavoriteItem
from datetime import datetime
from typing import List


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone_number: Optional[str]
    password: str
    age: Optional[int]
    profile_image: Optional[str]
    bio: str
    role: RoleChoices

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str


class CourseSchema(BaseModel):
    id: int
    course_name: str
    course_image: Optional[str]
    description: str
    category_id: int
    level: LevelChoices
    price: float
    created_by_id: int
    created_at: datetime
    updated_at: datetime


class LessonSchema(BaseModel):
    id: int
    title: str
    video_url: Optional[str]
    content: str
    course_id: int


class AssignmentSchema(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    course_id: int


class ExamSchema(BaseModel):
    id: int
    title:str
    course_id: int
    passing_score: ValidatorChoices
    duration: Optional[int]


class QuestionSchema(BaseModel):
    id: int
    text: str
    created_date: datetime
    difficulty_level: DifficultyLevelChoices
    exam_id: int


class OptionSchema(BaseModel):
    id: int
    question_id: int
    is_correct: bool


class CertificateSchema(BaseModel):
    id:int
    student_id: int
    course_id: int
    issued_at: datetime
    certificate_url: Optional[str]


class ReviewSchema(BaseModel):
    id: int
    user_id: int
    course_id: int
    rating: ValidatorChoices
    comment: str


class CartItemSchema(BaseModel):
    id: int
    course_id: int


class CartSchema(BaseModel):
    id: int
    users_id: int
    items: List[CartItemSchema] = []
    total_price: float


class CartItemCreateSchema(BaseModel):
    course_id: int


class FavoriteItemSchema(BaseModel):
    id: int
    course_id: int


class FavoriteSchema(BaseModel):
    id: int
    user_id: int
    fav_items: List[FavoriteItemSchema] =[]


class FavoriteItemCreateSchema(BaseModel):
    course_id: int