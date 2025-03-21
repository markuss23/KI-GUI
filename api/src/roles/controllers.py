from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from sqlalchemy.orm import Session

from api import models
from sqlalchemy import Delete, Select, select, update, insert, delete
from sqlalchemy.exc import IntegrityError
from api.src.roles.schemas import Role, RoleForm


def get_roles(sql: Session) -> list[Role]:
    try:
        stm: Select[tuple[models.Role]] = select(models.Role)
        results: Sequence[models.Role] = sql.execute(stm).scalars().all()

        return [Role.model_validate(result) for result in results]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_role(role_data: RoleForm, sql: Session) -> Role:
    try:
        stm: ReturningInsert[tuple[Role]] = (
            insert(models.Role).values(role_data.model_dump()).returning(models.Role)
        )
        result: models.Role = sql.execute(stm).scalar()
        sql.commit()

        return Role.model_validate(result)
    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def get_role(role_id: int, sql: Session) -> Role:
    try:
        result: models.Role = sql.execute(
            select(models.Role).where(models.Role.role_id == role_id)
        ).scalar()

        return Role.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_role(role_id: int, role_data: RoleForm, sql: Session) -> Role:
    try:
        stm: ReturningUpdate[tuple[Role]] = (
            update(models.Role)
            .where(models.Role.role_id == role_id)
            .values(role_data.model_dump())
            .returning(models.Role)
        )
        result: models.Role = sql.execute(stm).scalar()

        sql.commit()

        return Role.model_validate(result)

    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail=e.args[0]) from e
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def delete_role(role_id: int, sql: Session) -> None:
    try:
        stm: Delete = delete(models.Role).where(models.Role.role_id == role_id)

        sql.execute(stm)

        sql.commit()

    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e
