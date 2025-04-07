from fastapi import APIRouter

from api.database import SqlSessionDependency
from api.src.enrollments.annotations import ID_ENROLLMENT_PATH_ANNOTATION
from api.src.enrollments.controllers import (
    get_enrollments,
    create_enrollment,
    get_enrollment,
    update_enrollment,
    delete_enrollment,
)
from api.src.enrollments.schemas import Enrollment, EnrollmentForm

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.get("", operation_id="get_enrollments")
def endpoint_get_enrollments(
    sql: SqlSessionDependency,
) -> list[Enrollment]:
    return get_enrollments(sql)


@router.post("", status_code=201, operation_id="create_enrollment")
def endpoint_create_enrollment(
    enrollment_data: EnrollmentForm,
    sql: SqlSessionDependency,
) -> Enrollment:
    return create_enrollment(enrollment_data, sql)


@router.get("/{enrollment_id}", operation_id="get_enrollment")
def endpoint_get_enrollment(
    enrollment_id: ID_ENROLLMENT_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> Enrollment:
    return get_enrollment(enrollment_id, sql)


@router.put("/{enrollment_id}", status_code=200, operation_id="update_enrollment")
def endpoint_update_enrollment(
    enrollment_id: ID_ENROLLMENT_PATH_ANNOTATION,
    enrollment_data: EnrollmentForm,
    sql: SqlSessionDependency,
) -> Enrollment:
    return update_enrollment(enrollment_id, enrollment_data, sql)


@router.delete("/{enrollment_id}", status_code=204, operation_id="delete_enrollment")
def endpoint_delete_enrollment(
    enrollment_id: ID_ENROLLMENT_PATH_ANNOTATION,
    sql: SqlSessionDependency,
) -> None:
    return delete_enrollment(enrollment_id, sql)