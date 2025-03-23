from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.users.annotations import ID_USER_PATH_ANNOTATION
from api.src.users.controllers import create_user, get_user, get_users, update_user
from api.src.users.schemas import User, UserForm


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", operation_id="get_users")
def endpoint_get_users(
    sql: SqlSessionDependency,
) -> list[User]:
    return get_users(sql)


@router.post("", status_code=201, operation_id="create_user")
def endpoint_create_user(
    user_data: UserForm,
    sql: SqlSessionDependency,
) -> User:
    return create_user(user_data, sql)


@router.get("/{user_id}", operation_id="get_user")
def endpoint_get_user(
    user_id: ID_USER_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> User:
    return get_user(user_id, sql)


@router.put("/{user_id}", status_code=200, operation_id="update_user")
def endpoint_update_user(
    user_id: ID_USER_PATH_ANNOTATION,
    user_data: UserForm,
    sql: SqlSessionDependency,
) -> User:
    return update_user(user_id, user_data, sql)
