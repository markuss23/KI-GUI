from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy import Select, insert, update, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from sqlalchemy.exc import IntegrityError
from api.utils import validate_int

from api import models
from api.src.users.schemas import User, UserForm


def get_users(sql: Session) -> list[User]:
    try:
        stm: Select[tuple[models.User]] = select(models.User)
        results: Sequence[models.User] = sql.execute(stm).scalars().all()

        return [User.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_user(user_data: UserForm, sql: Session) -> User:
    try:

        if (
            sql.execute(
                select(models.Role).where(models.Role.role_id == validate_int(user_data.role_id))
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Role not found")

        stm: ReturningInsert[tuple[User]] = (
            insert(models.User).values(user_data.model_dump()).returning(models.User)
        )
        result: models.User = sql.execute(stm).scalar()
        sql.commit()

        return User.model_validate(result)
    except HTTPException as e:
        raise e

    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail="User already exists.") from e

    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def get_user(user_id: int, sql: Session) -> User:
    try:
        result: models.User = sql.execute(
            select(models.User).where(models.User.user_id == user_id)
        ).scalar()

        return User.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_user(user_id: int, user_data: UserForm, sql: Session) -> User:
    try:
        if (
            sql.execute(
                select(models.Role).where(models.Role.role_id == validate_int(user_data.role_id))
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Role not found")

        stm: ReturningUpdate[tuple[User]] = (
            update(models.User)
            .where(models.User.user_id == user_id)
            .values(user_data.model_dump())
            .returning(models.User)
        )
        result: models.User = sql.execute(stm).scalar()
        sql.commit()

        return User.model_validate(result)
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail="User already exists.") from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
