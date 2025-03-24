from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api import models
from api.database import SqlSessionDependency

from sqlalchemy import select


def is_valid_task_completion_id(
    task_completion_id: Annotated[
        int,
        Path(
            title="TaskCompletion ID",
            description="TaskCompletion ID",
            ge=1,
            le=9223372036854775000,  # 8 bytes int max value
        ),
    ],
    sql: SqlSessionDependency,
) -> int:
    try:
        if (
            sql.execute(
                select(models.TaskCompletion).where(
                    models.TaskCompletion.task_completion_id == task_completion_id
                )
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="TaskCompletion not found")

        return task_completion_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


ID_TASK_COMPLETION_PATH_ANNOTATION = Annotated[
    int, Depends(is_valid_task_completion_id)
]
