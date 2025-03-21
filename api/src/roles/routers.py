from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.roles.annotations import ID_ROLE_PATH_ANNOTATION
from api.src.roles.controllers import (
    create_role,
    delete_role,
    get_role,
    get_roles,
    update_role,
)
from api.src.roles.schemas import Role, RoleForm

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", operation_id="get_roles")
def endpoint_get_roles(
    sql: SqlSessionDependency,
) -> list[Role]:
    return get_roles(sql)


@router.post("", status_code=201, operation_id="create_role")
def endpoint_create_role(
    role_data: RoleForm,
    sql: SqlSessionDependency,
) -> Role:
    return create_role(role_data, sql)


@router.get("/{role_id}", operation_id="get_role")
def endpoint_get_role(
    role_id: ID_ROLE_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> Role:
    get_role(role_id, sql)


@router.put("/{role_id}", status_code=200, operation_id="update_role")
def endpoint_update_role(
    role_id: ID_ROLE_PATH_ANNOTATION,
    role_data: RoleForm,
    sql: SqlSessionDependency,
) -> Role:
    return update_role(role_id, role_data, sql)


@router.delete("/{role_id}", status_code=204, operation_id="delete_role")
def endpoint_delete_role(
    role_id: ID_ROLE_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_role(role_id, sql)
