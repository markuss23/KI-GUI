from fastapi import HTTPException


def validate_int(number: int) -> int:
    """
    Kvůli SQLite je potřeba validovat číslo, aby bylo v rozsahu 0-9223372036854775807.
    """

    try:
        if number > 9223372036854775000 or number < -9223372036854775000:
            raise ValueError("Number must be greater than 0")

        return number
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e) from e
