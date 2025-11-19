from course_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Text, DECIMAL, Boolean
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime
from passlib.hash import bcrypt



class ValidatorChoices(str, PyEnum):
    one = '1'
    two = '2'
    three = '3'
    four = '4'
    five = '5'


class RoleChoices(str, PyEnum):
    student = 'student'
    teacher = 'teacher'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(64))
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(Text)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), nullable=True, default=RoleChoices.student)
    created_user: Mapped['Course'] = relationship('Course', back_populates='created_by',
                                                  cascade='all, delete-orphan')
    student_review: Mapped['Review'] = relationship('Review', back_populates='user',
                                                    cascade='all, delete-orphan')
    students: Mapped['Certificate'] = relationship('Certificate', back_populates='student',
                                                   cascade='all, delete-orphan')
    tokens: Mapped['RefreshToken'] = relationship('RefreshToken', back_populates='user',
                                                  cascade='all, delete-orphan')
    cart_user: Mapped['Cart'] = relationship('Cart', back_populates='users',
                                             cascade='all, delete-orphan', uselist=False)
    fav_user: Mapped['Favorite'] = relationship('Favorite', back_populates='user',
                                                cascade='all, delete-orphan', uselist=False)


    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_passwords(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def __str__(self):
        return f'{self.first_name}, {self.username}, {self.role}'


class RefreshToken(Base):
    __tablename__ = 'RefreshToken'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship(UserProfile, back_populates='tokens')



class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(64), unique=True)
    category_course: Mapped[List['Course']] = relationship('Course', back_populates='category',
                                                           cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.category_name}'


class LevelChoices(str, PyEnum):
    beginner = 'beginner'
    intermediate = 'intermediate'
    advanced = 'advanced'


class Course(Base):
    __tablename__ = 'course'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(140))
    course_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(Category, back_populates='category_course')
    level: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices), nullable=True, default=LevelChoices.beginner)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    created_by_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    created_by: Mapped[UserProfile] = relationship(UserProfile, back_populates='created_user')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course_lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='course',
                                                    cascade='all, delete-orphan')
    course_assignments: Mapped[List['Assignment']] = relationship('Assignment', back_populates='course',
                                                    cascade='all, delete-orphan')
    course_exam: Mapped[List['Exam']] = relationship('Exam', back_populates='course',
                                                     cascade='all, delete-orphan')
    course_rating: Mapped['Review'] = relationship('Review', back_populates='course',
                                                   cascade='all, delete-orphan')
    course_certificate: Mapped['Certificate'] = relationship('Certificate', back_populates='course',
                                                   cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.course_name}, {self.price}'


class Lesson(Base):
    __tablename__ = 'lesson'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(140))
    video_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course', back_populates='course_lessons')

    def __str__(self):
        return f'{self.title}, {self.course_id}'


class Assignment(Base):
    __tablename__ = 'assignment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[datetime] = mapped_column(DateTime)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course', back_populates='course_assignments')

    def __str__(self):
        return f'{self.title}, {self.due_date}'


class Exam(Base):
    __tablename__ = 'exam'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course', back_populates='course_exam')
    passing_score: Mapped[ValidatorChoices] = mapped_column(Enum(ValidatorChoices), nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exam_questions: Mapped[List['Question']] = relationship('Question', back_populates='exam',
                                                            cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.title}, {self.passing_score}'


class DifficultyLevelChoices(str,PyEnum):
    easy = 'easy'
    medium = 'medium'
    difficult = 'difficult'


class Question(Base):
    __tablename__ = 'question'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(200))
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    difficulty_level: Mapped[DifficultyLevelChoices] = mapped_column(Enum(DifficultyLevelChoices), nullable=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey('exam.id'))
    exam: Mapped[Exam] = relationship('Exam', back_populates='exam_questions')
    question_options: Mapped[List['Option']] = relationship('Option', back_populates='question',
                                                      cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.id}, {self.difficulty_level}, {self.exam_id}, {self.text}'


class Option(Base):
    __tablename__ = 'options'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('question.id'))
    question: Mapped[Question] = relationship('Question', back_populates='question_options')
    is_correct: Mapped[bool] = mapped_column(Boolean)

    def __str__(self):
        return f'{self.question_id}, {self.is_correct}'


class Certificate(Base):
    __tablename__ = 'certificate'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    student: Mapped[UserProfile] = relationship('UserProfile', back_populates='students')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course', back_populates='course_certificate')
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    certificate_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __str__(self):
        return f'{self.student_id}, {self.course_id}, {self.issued_at}'


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='student_review')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course', back_populates='course_rating')
    rating: Mapped[ValidatorChoices] = mapped_column(Enum(ValidatorChoices), nullable=True)
    comment: Mapped[str] = mapped_column(Text)

    def __str__(self):
        return f'{self.user_id}, {self.rating}, {self.course_id}'


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)
    users: Mapped[UserProfile] = relationship('UserProfile', back_populates='cart_user')
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                            cascade='all, delete-orphan')


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='fav_user')
    fav_items: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='fav',
                                                           cascade='all, delete-orphan')


class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fav_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    fav: Mapped[Favorite] = relationship('Favorite', back_populates='fav_items')
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    course: Mapped[Course] = relationship('Course')