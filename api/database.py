from typing import Annotated, Any
from collections.abc import Generator
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


from api.config import settings
from api.models import Base

"""
Tento soubor definuje připojení k databázi SQLite pomocí SQLAlchemy.
Používá se zde SQLite jako databázový systém a SQLAlchemy jako ORM (Object-Relational Mapping) knihovna.
Databáze je uložena v souboru s názvem určeným v konfiguračním souboru.
Vytváří se zde také funkce pro inicializaci databáze a pro získání relace k databázi.
Funkce `get_sql` vrací generátor, který poskytuje relaci k databázi.
Tento generátor je použit jako závislost v endpointu FastAPI.
Tento soubor také definuje `SqlSessionDependency`, Anotace Session závislost generátoru `get_sql`.
Tento soubor je důležitý pro správu připojení k databázi a pro práci s ORM modely.
Funkce `init_db` inicializuje databázi a vytváří všechny tabulky definované v modelech.

"""
sqlite_file_name: str = settings.sql.name
sqlite_url: str = f"sqlite:///{sqlite_file_name}.db"

connect_args: dict[str, bool] = {"check_same_thread": False}

engine: Engine = create_engine(sqlite_url, connect_args=connect_args)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_sql() -> Generator[Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    init_engine: Engine = create_engine(sqlite_url, connect_args=connect_args)

    Base.metadata.create_all(bind=engine)

    init_engine.dispose()


SqlSessionDependency = Annotated[Session, Depends(get_sql)]
