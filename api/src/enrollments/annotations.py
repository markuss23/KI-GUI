from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api import models
from api.database import SqlSessionDependency

from sqlalchemy import select


def is_valid_enrollment_id(
    enrollment_id: Annotated[
        int,
        Path(
            title="Enrollment ID",
            description="Enrollment ID",
            ge=1,
            le=9223372036854775807,  # 8 bytes int max value
        ),
    ],
    sql: SqlSessionDependency,
) -> int:
    try:
        if (
            sql.execute(
                select(models.Enrollment).where(models.Enrollment.enrollment_id == enrollment_id)
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Enrollment not found")

        return enrollment_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


ID_ENROLLMENT_PATH_ANNOTATION = Annotated[int, Depends(is_valid_enrollment_id)]

