from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.courses.annotations import ID_COURSE_PATH_ANNOTATION
from api.src.courses.controllers import (
    create_course,
    delete_course,
    get_course,
    get_courses,
    update_course,
)
from api.src.courses.schemas import Course, CourseForm

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", operation_id="get_courses")
def endpoint_get_courses(
    sql: SqlSessionDependency,
) -> list[Course]:
    return get_courses(sql)


@router.post("", status_code=201, operation_id="create_course")
def endpoint_create_course(
    course_data: CourseForm,
    sql: SqlSessionDependency,
) -> Course:
    return create_course(course_data, sql)


@router.get("/{course_id}", operation_id="get_course")
def endpoint_get_course(
    course_id: ID_COURSE_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> Course:
    return get_course(course_id, sql)


@router.put("/{course_id}", status_code=200, operation_id="update_course")
def endpoint_update_course(
    course_id: ID_COURSE_PATH_ANNOTATION,
    course_data: CourseForm,
    sql: SqlSessionDependency,
) -> Course:
    return update_course(course_id, course_data, sql)


@router.delete("/{course_id}", status_code=204, operation_id="delete_course")
def endpoint_delete_course(
    course_id: ID_COURSE_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_course(course_id, sql)
