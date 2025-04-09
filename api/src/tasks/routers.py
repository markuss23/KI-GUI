from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.tasks.annotations import ID_TASK_PATH_ANNOTATION
from api.src.tasks.controllers import (
    get_tasks,
    create_task,
    get_task,
    update_task,
    delete_task,
)
from api.src.tasks.schemas import Task, TaskForm

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", operation_id="get_tasks")
def endpoint_get_tasks(
    sql: SqlSessionDependency,
) -> list[Task]:
    return get_tasks(sql)


@router.post("", status_code=201, operation_id="create_task")
def endpoint_create_task(
    task_data: TaskForm,
    sql: SqlSessionDependency,
) -> Task:
    return create_task(task_data, sql)


@router.get("/{task_id}", operation_id="get_task")
def endpoint_get_task(
    task_id: ID_TASK_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> Task:
    return get_task(task_id, sql)


@router.put("/{task_id}", status_code=200, operation_id="update_task")
def endpoint_update_task(
    task_id: ID_TASK_PATH_ANNOTATION,
    task_data: TaskForm,
    sql: SqlSessionDependency,
) -> Task:
    return update_task(task_id, task_data, sql)


@router.delete("/{task_id}", status_code=204, operation_id="delete_task")
def endpoint_delete_task(
    task_id: ID_TASK_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_task(task_id, sql)
