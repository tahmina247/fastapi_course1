from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from course_app.db.database import SessionLocal
from course_app.api.endpoints import auth, assignment, category, certificate, course, exam, lesson, option, question, review, oauth, cart, favorite
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from course_app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from fastapi_pagination import add_pagination


async def init_redis():
    return aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await init_redis()
    await FastAPILimiter.init(redis_client)
    yield
    await redis_client.close()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


course_app = FastAPI(title='course_site', lifespan=lifespan)
course_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(course_app)
add_pagination(course_app)


course_app.include_router(auth.auth_router)
course_app.include_router(oauth.oauth_router)
course_app.include_router(cart.cart_router)
course_app.include_router(favorite.favorite_router)
course_app.include_router(assignment.assignment_router)
course_app.include_router(category.category_router)
course_app.include_router(certificate.certificate_router)
course_app.include_router(course.course_router)
course_app.include_router(exam.exam_router)
course_app.include_router(lesson.lesson_router)
course_app.include_router(question.question_router)
course_app.include_router(option.option_router)
course_app.include_router(review.review_router)



if __name__ == "__main__":
    uvicorn.run(course_app, host="127.0.0.1", port=9000)