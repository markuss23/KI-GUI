from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api import models
from api.database import SqlSessionDependency

from sqlalchemy import select


def is_valid_role_id(role_id: int, sql: SqlSessionDependency) -> int:
    try:
        if (
            sql.execute(
                select(models.Role).where(models.Role.role_id == role_id)
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="Role not found")

        return role_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


ID_ROLE_PATH_ANNOTATION = Annotated[
    int,
    Path(
        title="Role ID",
        description="Role ID",
        gt=0,
    ),
    Depends(is_valid_role_id),
]
