from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    name = Column(String(length=16), nullable=False, unique=True)
    description = Column(String(length=255), nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    role = relationship("Role", back_populates="users")
    created_courses = relationship("Course", back_populates="teacher")
    student_enrollments = relationship(
        "Enrollment", foreign_keys="Enrollment.student_id", back_populates="student"
    )
    assigned_enrollments = relationship(
        "Enrollment", foreign_keys="Enrollment.assigner_id", back_populates="assigner"
    )


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    deadline_in_days = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    teacher = relationship("User", back_populates="created_courses")
    tasks = relationship("Task", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    category = relationship("Category", back_populates="courses")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    course = relationship("Course", back_populates="tasks")
    task_completions = relationship("TaskCompletion", back_populates="task")


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    assigner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    enrolled_at = Column(Date, nullable=False)
    deadline = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    student = relationship(
        "User", foreign_keys=[student_id], back_populates="student_enrollments"
    )
    assigner = relationship(
        "User", foreign_keys=[assigner_id], back_populates="assigned_enrollments"
    )
    course = relationship("Course", back_populates="enrollments")
    task_completions = relationship("TaskCompletion", back_populates="enrollment")


class TaskCompletion(Base):
    __tablename__ = "task_completions"

    task_completion_id = Column(Integer, primary_key=True, nullable=False)
    enrollment_id = Column(
        Integer, ForeignKey("enrollments.enrollment_id"), nullable=False
    )
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    enrollment = relationship("Enrollment", back_populates="task_completions")
    task = relationship("Task", back_populates="task_completions")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    courses = relationship("Course", back_populates="category")
