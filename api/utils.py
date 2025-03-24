from fastapi import HTTPException


def validate_int(number: int) -> int:
    
    try:
        if number > 9223372036854775807 or number < -9223372036854775807:
            raise ValueError("Number must be greater than 0")

        return number
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e) from e
