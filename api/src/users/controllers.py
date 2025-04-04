from collections.abc import Sequence
from fastapi import HTTPException
from sqlalchemy import Select, insert, update, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate
from sqlalchemy.exc import IntegrityError
from api.utils import validate_int

from api import models
from api.src.users.schemas import User, UserForm


"""
Controller pro uživatelské operace
Tento controller obsahuje funkce pro CRUD operace s uživateli.
"""


def get_users(sql: Session) -> list[User]:
    try:
        # definice stm - klasický SQL dotaz
        # SELECT * FROM users
        stm: Select[tuple[models.User]] = select(models.User)
        # provedení dotazu
        results: Sequence[models.User] = sql.execute(stm).scalars().all()

        # zpracování výsledků
        # model_validate je metoda z Pydantic, která validuje data podle definice modelu
        # a převádí je na instanci modelu
        # v tomto případě převádíme každý výsledek na instanci User
        # a vracíme seznam těchto instancí
        return [User.model_validate(result) for result in results]

    # Pokud dojde k nějaké chybě, vytiskneme ji do konzole
    # může třeba dojít , že databáze není dostupná
    # nebo že došlo k chybě při provádění dotazu
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def create_user(user_data: UserForm, sql: Session) -> User:
    try:
        # kontrola, zda role existuje
        # pokud neexistuje, vyvolá HTTP výjimku 404 (Not Found)
        # pokud existuje, pokračujeme dál
        if (
            sql.execute(
                select(models.Role).where(
                    models.Role.role_id == validate_int(user_data.role_id)
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Role not found")

        # definice stm - klasický SQL dotaz
        # INSERT INTO users (name, email, password, role_id) VALUES (...)
        # vracíme vložený záznam
        stm: ReturningInsert[tuple[User]] = (
            insert(models.User).values(user_data.model_dump()).returning(models.User)
        )
        # provedení dotazu
        # result je výsledek provedení dotazu
        # jelikož v stm máme definováno, že vracíme vložený záznam
        # tak result bude obsahovat vložený záznam
        result: models.User = sql.execute(stm).scalar()

        # commitnutí transakce
        # Pokud dojde k chybě, transakce se neprovede
        # a databáze se vrátí do původního stavu
        # pokud vše proběhne v pořádku, transakce se commitne
        # Kdyby se to necommitlo, tak by se změny neprojevily v databázi
        # a uživatel by nebyl vytvořen
        # ačkoliv by se to tak zdálo
        sql.commit()
        # převod výsledku na instanci User
        return User.model_validate(result)

    # Pokud dojde k HTTP výjimce, vyvoláme ji
    except HTTPException as e:
        raise e

    # Pokud dojde k chybě při provádění dotazu
    # například pokud uživatel s tímto emailem již existuje
    except IntegrityError as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=409, detail="User already exists.") from e
    # Pokud dojde k jiné chybě
    except Exception as e:
        sql.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def get_user(user_id: int, sql: Session) -> User:
    try:
        # Ziskání uživatele podle ID
        # SELECT * FROM users WHERE user_id = user_id
        # provedení dotazu
        # result je výsledek provedení dotazu
        result: models.User = sql.execute(
            select(models.User).where(models.User.user_id == user_id)
        ).scalar()

        return User.model_validate(result)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


def update_user(user_id: int, user_data: UserForm, sql: Session) -> User:
    try:
        # kontrola, zda role existuje
        # pokud neexistuje, vyvolá HTTP výjimku 404 (Not Found)
        if (
            sql.execute(
                select(models.Role).where(
                    models.Role.role_id == validate_int(user_data.role_id)
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Role not found")

        # definice stm - klasický SQL dotaz
        # UPDATE users SET name = ..., email = ..., password = ..., role_id = ... WHERE user_id = user_id
        # vracíme aktualizovaný záznam
        # values(user_data.model_dump()) - převádí data na slovník
        # a předáváme je do dotazu
        # vracíme aktualizovaný záznam
        stm: ReturningUpdate[tuple[User]] = (
            update(models.User)
            .where(models.User.user_id == user_id)
            .values(user_data.model_dump())
            .returning(models.User)
        )
        # provedení dotazu
        # result je výsledek provedení dotazu
        result: models.User = sql.execute(stm).scalar()

        # commitnutí transakce
        sql.commit()

        # převod výsledku na instanci User
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
