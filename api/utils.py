from fastapi import HTTPException


def validate_int(number: int) -> int:
    try:
        number_str = str(number)
        number_int = int(number_str, base=8)
        return number_int
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid number") from e
