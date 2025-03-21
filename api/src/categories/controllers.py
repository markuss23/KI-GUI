from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Select, select, update, insert
from sqlalchemy.exc import IntegrityError
from api.src.categories.schemas import Category, CategoryForm


def get_categories(sql: Session) -> list[Category]:
    try:
        stm: Select[tuple[models.Category]] = select(models.Category)
        results: Sequence[models.Category] = sql.execute(stm).scalars().all()

        return [Category.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_category(category_data: CategoryForm, sql: Session) -> Category:
    try:
        stm: ReturningInsert[tuple[Category]] = (
            insert(models.Category)
            .values(category_data.model_dump())
            .returning(models.Category)
        )
        result: models.Category = sql.execute(stm).scalar()
        sql.commit()

        return Category.model_validate(result)
    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def get_category(category_id: int, sql: Session) -> Category:
    try:
        result: models.Category = sql.execute(
            select(models.Category).where(models.Category.category_id == category_id)
        ).scalar()

        return Category.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_category(
    category_id: int, category_data: CategoryForm, sql: Session
) -> Category:
    try:
        stm: ReturningUpdate[tuple[Category]] = (
            update(models.Category)
            .where(models.Category.category_id == category_id)
            .values(category_data.model_dump())
            .returning(models.Category)
        )
        result: models.Category = sql.execute(stm).scalar()

        sql.commit()

        return Category.model_validate(result)

    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def delete_category(category_id: int, sql: Session) -> None:
    try:
        stm: ReturningUpdate[tuple[Category]] = (
            update(models.Category)
            .where(models.Category.category_id == category_id)
            .values(is_active=False)
            .returning(models.Category)
        )
        sql.execute(stm)
        sql.commit()
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
