from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.users.annotations import ID_USER_PATH_ANNOTATION
from api.src.users.controllers import create_user, get_user, get_users, update_user
from api.src.users.schemas import User, UserForm


"""
Routers pro uživatelské API
Toto je FastAPI router pro uživatelské API.
Zde definujeme všechny routy pro uživatelské API.
Všechny routy jsou pod prefixem /users.
"""

# Vytvoření routeru pro uživatelské API
router = APIRouter(prefix="/users", tags=["Users"])


# Definice routeru pro získání uživatelů
# sql: SqlSessionDependency je závislost pro SQLAlchemy session
# -> list[User] je návratový typ funkce - propíše se do OpenAPI
@router.get("", operation_id="get_users")
def endpoint_get_users(
    sql: SqlSessionDependency,
) -> list[User]:
    return get_users(sql)


# Definice routeru pro vytvoření uživatele
# sql: SqlSessionDependency je závislost pro SQLAlchemy session
# user_data: UserForm je vstupní datový typ pro vytvoření uživatele
# -> User je návratový typ funkce - propíše se do OpenAPI
# -> 201 je status code pro úspěšné vytvoření uživatele
@router.post("", status_code=201, operation_id="create_user")
def endpoint_create_user(
    user_data: UserForm,
    sql: SqlSessionDependency,
) -> User:
    return create_user(user_data, sql)


# Definice routeru pro získání uživatele podle ID
# sql: SqlSessionDependency je závislost pro SQLAlchemy session
# user_id: ID_USER_PATH_ANNOTATION je vstupní datový typ pro ID uživatele
# ID_USER_PATH_ANNOTATION je anotace pro validaci ID uživatele
# -> User je návratový typ funkce - propíše se do OpenAPI
@router.get("/{user_id}", operation_id="get_user")
def endpoint_get_user(
    user_id: ID_USER_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> User:
    return get_user(user_id, sql)


# Definice routeru pro aktualizaci uživatele podle ID
# sql: SqlSessionDependency je závislost pro SQLAlchemy session
# user_id: ID_USER_PATH_ANNOTATION je vstupní datový typ pro ID uživatele
# user_data: UserForm je vstupní datový typ pro aktualizaci uživatele
# ID_USER_PATH_ANNOTATION je anotace pro validaci ID uživatele
# -> User je návratový typ funkce - propíše se do OpenAPI
@router.put("/{user_id}", status_code=200, operation_id="update_user")
def endpoint_update_user(
    user_id: ID_USER_PATH_ANNOTATION,
    user_data: UserForm,
    sql: SqlSessionDependency,
) -> User:
    return update_user(user_id, user_data, sql)
