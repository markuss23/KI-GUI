from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.categories.annotations import ID_CATEGORY_PATH_ANNOTATION
from api.src.categories.controllers import (
    create_category,
    delete_category,
    get_category,
    get_categories,
    update_category,
)
from api.src.categories.schemas import Category, CategoryForm

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", operation_id="get_categories")
def endpoint_get_categories(
    sql: SqlSessionDependency,
) -> list[Category]:
    return get_categories(sql)


@router.post("", status_code=201, operation_id="create_category")
def endpoint_create_category(
    category_data: CategoryForm,
    sql: SqlSessionDependency,
) -> Category:
    return create_category(category_data, sql)


@router.get("/{category_id}", operation_id="get_category")
def endpoint_get_category(
    category_id: ID_CATEGORY_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> Category:
    return get_category(category_id, sql)


@router.put("/{category_id}", status_code=200, operation_id="update_category")
def endpoint_update_category(
    category_id: ID_CATEGORY_PATH_ANNOTATION,
    category_data: CategoryForm,
    sql: SqlSessionDependency,
) -> Category:
    return update_category(category_id, category_data, sql)


@router.delete("/{category_id}", status_code=204, operation_id="delete_category")
def endpoint_delete_category(
    category_id: ID_CATEGORY_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_category(category_id, sql)
