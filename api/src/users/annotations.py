from fastapi import Depends, HTTPException, Path
from sqlalchemy import select
from typing import Annotated

from api import models
from api.database import SqlSessionDependency

"""
Anotace pro uživatelské ID

Jedná se o funkci, která očekává Path parametr `user_id` a SQL session jako depends.
Funkce provádí dotaz do databáze a ověřuje, zda uživatelské ID existuje.

Výhodou této funkce je, že to spadne sem dříve, než se dostaneme do controlleru.

Pokud ID neexistuje, vyvolá HTTP výjimku 404 (Not Found).
Pokud dojde k jiné chybě, vyvolá HTTP výjimku 500 (Internal Server Error).
"""


def is_valid_user_id(
    user_id: Annotated[
        int,
        Path(
            title="User ID",
            description="User ID",
            ge=1,
            le=9223372036854775000,  # 8 bytes int max value
        ),
    ],
    sql: SqlSessionDependency,
) -> int:
    try:
        if (
            sql.execute(
                select(models.User).where(models.User.user_id == user_id)
            ).scalar_one_or_none()
            is None
        ):
            raise HTTPException(status_code=404, detail="User not found")

        return user_id
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Unexpected error occurs.") from e


ID_USER_PATH_ANNOTATION = Annotated[int, Depends(is_valid_user_id)]
