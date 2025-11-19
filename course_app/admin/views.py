from course_app.db.models import UserProfile, Category, Course, Lesson, Assignment, Exam, Question, Option, Certificate, Review
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.role]
    name = 'User'
    name_plural = 'Users'


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.course_name]


class LessonAdmin(ModelView, model=Lesson):
    column_list = [Lesson.id, Lesson.title, Lesson.course_id]


class AssignmentAdmin(ModelView, model=Assignment):
    column_list = [Assignment.id, Assignment.title]


class ExamAdmin(ModelView, model=Exam):
    column_list = [Exam.id, Exam.title]


class QuestionAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.difficulty_level, Question.text, Question.exam_id]


class OptionAdmin(ModelView, model=Option):
    column_list = [Option.id, Option.is_correct]


class CertificateAdmin(ModelView, model=Certificate):
    column_list = [Certificate.id, Certificate.student_id]


class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.rating, Review.course_id]