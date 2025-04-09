from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Row, Select, select, update, insert
from sqlalchemy.exc import IntegrityError
from api.src.task_completions.schemas import TaskCompletion, TaskCompletionForm
from sqlalchemy.sql.expression import exists

from api.utils import validate_int


def get_task_completions(sql: Session) -> list[TaskCompletion]:
    try:
        stm: Select[tuple[models.TaskCompletion]] = select(models.TaskCompletion)
        results: Sequence[models.TaskCompletion] = sql.execute(stm).scalars().all()

        return [TaskCompletion.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_task_completion(
    task_completion_data: TaskCompletionForm, sql: Session
) -> TaskCompletion:
    try:
        check: Row[tuple[bool, bool]] = sql.execute(
            select(
                exists()
                .where(
                    models.Enrollment.enrollment_id
                    == validate_int(task_completion_data.enrollment_id)
                )
                .label("enrollment_exists"),
                exists()
                .where(
                    models.Task.task_id == validate_int(task_completion_data.task_id)
                )
                .label("task_exists"),
            )
        ).one()

        if not check.enrollment_exists:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        if not check.task_exists:
            raise HTTPException(status_code=404, detail="Task not found")

        stm: ReturningInsert[tuple[TaskCompletion]] = (
            insert(models.TaskCompletion)
            .values(task_completion_data.model_dump())
            .returning(models.TaskCompletion)
        )
        result: models.TaskCompletion = sql.execute(stm).scalar()
        sql.commit()

        return TaskCompletion.model_validate(result)

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


def get_task_completion(task_completion_id: int, sql: Session) -> TaskCompletion:
    try:
        result: models.TaskCompletion = sql.execute(
            select(models.TaskCompletion).where(
                models.TaskCompletion.task_completion_id == task_completion_id
            )
        ).scalar()

        return TaskCompletion.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_task_completion(
    task_completion_id: int, task_completion_data: TaskCompletionForm, sql: Session
) -> TaskCompletion:
    try:
        check: Row[tuple[bool, bool]] = sql.execute(
            select(
                exists()
                .where(
                    models.Enrollment.enrollment_id
                    == validate_int(task_completion_data.enrollment_id)
                )
                .label("enrollment_exists"),
                exists()
                .where(models.Task.task_id == task_completion_data.task_id)
                .label("task_exists"),
            )
        ).one()

        if not check.enrollment_exists:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        if not check.task_exists:
            raise HTTPException(status_code=404, detail="Task not found")

        stm: ReturningUpdate[tuple[TaskCompletion]] = (
            update(models.TaskCompletion)
            .where(models.TaskCompletion.task_completion_id == task_completion_id)
            .values(task_completion_data.model_dump())
            .returning(models.TaskCompletion)
        )
        result: models.TaskCompletion = sql.execute(stm).scalar()

        sql.commit()

        return TaskCompletion.model_validate(result)

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


def delete_task_completion(task_completion_id: int, sql: Session) -> None:
    try:
        stm: ReturningUpdate[tuple[TaskCompletion]] = (
            update(models.TaskCompletion)
            .where(models.TaskCompletion.task_completion_id == task_completion_id)
            .values(is_active=False)
            .returning(models.TaskCompletion)
        )

        sql.execute(stm)

        sql.commit()

    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
