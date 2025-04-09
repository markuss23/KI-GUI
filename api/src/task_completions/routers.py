from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.task_completions.annotations import ID_TASK_COMPLETION_PATH_ANNOTATION
from api.src.task_completions.controllers import (
    create_task_completion,
    delete_task_completion,
    get_task_completion,
    get_task_completions,
    update_task_completion,
)
from api.src.task_completions.schemas import TaskCompletion, TaskCompletionForm

router = APIRouter(prefix="/task_completions", tags=["Task Completions"])


@router.get("", operation_id="get_task_completions")
def endpoint_get_task_completions(
    sql: SqlSessionDependency,
) -> list[TaskCompletion]:
    return get_task_completions(sql)


@router.post("", status_code=201, operation_id="create_task_completion")
def endpoint_create_task_completion(
    task_completion_data: TaskCompletionForm,
    sql: SqlSessionDependency,
) -> TaskCompletion:
    return create_task_completion(task_completion_data, sql)


@router.get("/{task_completion_id}", operation_id="get_task_completion")
def endpoint_get_task_completion(
    task_completion_id: ID_TASK_COMPLETION_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> TaskCompletion:
    return get_task_completion(task_completion_id, sql)


@router.put("/{task_completion_id}", status_code=200, operation_id="update_task_completion")
def endpoint_update_task_completion(
    task_completion_id: ID_TASK_COMPLETION_PATH_ANNOTATION,
    task_completion_data: TaskCompletionForm,
    sql: SqlSessionDependency,
) -> TaskCompletion:
    return update_task_completion(task_completion_id, task_completion_data, sql)


@router.delete("/{task_completion_id}", status_code=204, operation_id="delete_task_completion")
def endpoint_delete_task_completion(
    task_completion_id: ID_TASK_COMPLETION_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_task_completion(task_completion_id, sql)
