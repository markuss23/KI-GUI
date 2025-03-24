from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Select, select, update, insert
from sqlalchemy.exc import IntegrityError
from api.src.enrollments.schemas import Enrollment, EnrollmentForm


def get_enrollments(sql: Session) -> list[Enrollment]:
    try:
        stm: Select[tuple[models.Enrollment]] = select(models.Enrollment)
        results: Sequence[models.Enrollment] = sql.execute(stm).scalars().all()

        return [Enrollment.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_enrollment(enrollment_data: EnrollmentForm, sql: Session) -> Enrollment:
    try:
        if (
            sql.execute(
                select(models.User).where(
                    models.User.user_id == enrollment_data.student_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {enrollment_data.student_id} not found",
            )
        if (
            sql.execute(
                select(models.User).where(
                    models.User.user_id == enrollment_data.assigner_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Assigner with ID {enrollment_data.assigner_id} not found",
            )
        if (
            sql.execute(
                select(models.Course
                       ).where(
                    models.Course.course_id == enrollment_data.course_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Course with ID {enrollment_data.course_id} not found",
            )

        stm: ReturningInsert[tuple[models.Enrollment]] = (
            insert(models.Enrollment).values(enrollment_data.model_dump()).returning(models.Enrollment)
        )
        result: models.Enrollment = sql.execute(stm).scalar()
        sql.commit()

        return Enrollment.model_validate(result)

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


def get_enrollment(enrollment_id: int, sql: Session) -> Enrollment:
    try:
        result: models.Enrollment = sql.execute(
            select(models.Enrollment).where(models.Enrollment.enrollment_id == enrollment_id)
        ).scalar()

        return Enrollment.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_enrollment(enrollment_id: int, enrollment_data: EnrollmentForm, sql: Session) -> Enrollment:
    try:
        if (
            sql.execute(
                select(models.User).where(
                    models.User.user_id == enrollment_data.student_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {enrollment_data.student_id} not found",
            )
        if (
            sql.execute(
                select(models.User).where(
                    models.User.user_id == enrollment_data.assigner_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Assigner with ID {enrollment_data.assigner_id} not found",
            )
        if (
            sql.execute(
                select(models.Course).where(
                    models.Course.course_id == enrollment_data.course_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Course with ID {enrollment_data.course_id} not found",
            )
        
        stm: ReturningUpdate[tuple[Enrollment]] = (
            update(models.Enrollment)
            .where(models.Enrollment.enrollment_id == enrollment_id)
            .values(enrollment_data.model_dump())
            .returning(models.Enrollment)
        )
        result: models.Enrollment = sql.execute(stm).scalar()

        sql.commit()

        return Enrollment.model_validate(result)
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def delete_enrollment(enrollment_id: int, sql: Session) -> None:
    try:
        stm: ReturningUpdate[tuple[Enrollment]] = (
            update(models.Enrollment)
            .where(models.Enrollment.enrollment_id == enrollment_id)
            .values(is_active=False)
            .returning(models.Enrollment)
        )
        sql.execute(stm)
        sql.commit()
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
