from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api import models
from api.database import SqlSessionDependency

from sqlalchemy import select


def is_valid_course_id(
    course_id: Annotated[
        int,
        Path(
            title="Course ID",
            description="Course ID",
            ge=1,
            le=9223372036854775807,  # 8 bytes int max value
        ),
    ],
    sql: SqlSessionDependency,
) -> int:
    try:
        if (
            sql.execute(
                select(models.Course).where(models.Course.course_id == course_id)
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Course not found")

        return course_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


ID_COURSE_PATH_ANNOTATION = Annotated[int, Depends(is_valid_course_id)]
