from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Select, select, update, insert
from sqlalchemy.exc import IntegrityError
from api.src.courses.schemas import Course, CourseForm


def get_courses(sql: Session) -> list[Course]:
    try:
        stm: Select[tuple[models.Course]] = select(models.Course)
        results: Sequence[models.Course] = sql.execute(stm).scalars().all()

        return [Course.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_course(course_data: CourseForm, sql: Session) -> Course:
    try:
        if (
            sql.execute(
                select(models.User).where(models.User.user_id == course_data.teacher_id)
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Teacher with ID {course_data.teacher_id} not found",
            )

        if (
            sql.execute(
                select(models.Category).where(
                    models.Category.category_id == course_data.category_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Category with ID {course_data.category_id} not found",
            )

        stm: ReturningInsert[tuple[models.Course]] = (
            insert(models.Course)
            .values(course_data.model_dump())
            .returning(models.Course)
        )
        result: models.Course = sql.execute(stm).scalar()
        sql.commit()

        return Course.model_validate(result)

    except HTTPException:
        raise

    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def get_course(course_id: int, sql: Session) -> Course:
    try:
        result: models.Course = sql.execute(
            select(models.Course).where(models.Course.course_id == course_id)
        ).scalar()

        return Course.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_course(course_id: int, course_data: CourseForm, sql: Session) -> Course:
    try:
        stm: ReturningUpdate[tuple[Course]] = (
            update(models.Course)
            .where(models.Course.course_id == course_id)
            .values(course_data.model_dump())
            .returning(models.Course)
        )
        result: models.Course = sql.execute(stm).scalar()

        sql.commit()

        return Course.model_validate(result)

    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def delete_course(course_id: int, sql: Session) -> None:
    try:
        stm: ReturningUpdate[tuple[Course]] = (
            update(models.Course)
            .where(models.Course.course_id == course_id)
            .values(is_active=False)
            .returning(models.Course)
        )
        sql.execute(stm)
        sql.commit()
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
