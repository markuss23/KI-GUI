from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api import models
from api.database import SqlSessionDependency

from sqlalchemy import select

from api.utils import validate_int


def is_valid_role_id(
    role_id: Annotated[
        int,
        Path(
            title="Role ID",
            description="Role ID",
            ge=1,
            le=9223372036854775807,  # 8 bytes int max value
        ),
    ],
    sql: SqlSessionDependency,
) -> int:
    try:
        if (
            sql.execute(
                select(models.Role).where(models.Role.role_id == validate_int(role_id))
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


ID_ROLE_PATH_ANNOTATION = Annotated[int, Depends(is_valid_role_id)]
