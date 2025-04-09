from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Select, select, update, insert
from sqlalchemy.exc import IntegrityError
from api.src.tasks.schemas import Task, TaskForm
from api.utils import validate_int


def get_tasks(sql: Session) -> list[Task]:
    try:
        stm: Select[tuple[models.Task]] = select(models.Task)
        results: Sequence[models.Task] = sql.execute(stm).scalars().all()

        return [Task.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_task(task_data: TaskForm, sql: Session) -> Task:
    try:
        if (
            sql.execute(
                select(models.Course).where(
                    models.Course.course_id == validate_int(task_data.course_id)
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Course with ID {task_data.course_id} not found",
            )

        stm: ReturningInsert[tuple[models.Task]] = (
            insert(models.Task).values(task_data.model_dump()).returning(models.Task)
        )
        result: models.Course = sql.execute(stm).scalar()
        sql.commit()

        return Task.model_validate(result)

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


def get_task(task_id: int, sql: Session) -> Task:
    try:
        result: models.Task = sql.execute(
            select(models.Task).where(models.Task.task_id == task_id)
        ).scalar()

        return Task.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_task(task_id: int, task_data: TaskForm, sql: Session) -> Task:
    try:
        if (
            sql.execute(
                select(models.Course).where(
                    models.Course.course_id == validate_int(task_data.course_id)
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(
                status_code=404,
                detail=f"Course with ID {task_data.course_id} not found",
            )
        
        stm: ReturningUpdate[tuple[Task]] = (
            update(models.Task)
            .where(models.Task.task_id == task_id)
            .values(task_data.model_dump())
            .returning(models.Task)
        )
        result: models.Task = sql.execute(stm).scalar()

        sql.commit()

        return Task.model_validate(result)
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


def delete_task(task_id: int, sql: Session) -> None:
    try:
        stm: ReturningUpdate[tuple[Task]] = (
            update(models.Task)
            .where(models.Task.task_id == task_id)
            .values(is_active=False)
            .returning(models.Task)
        )
        sql.execute(stm)
        sql.commit()
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
