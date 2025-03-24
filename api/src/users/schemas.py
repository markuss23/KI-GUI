from pydantic import BaseModel, ConfigDict, Field, field_validator
import hashlib

from api.src.roles.schemas import Role


class UserBase(BaseModel):
    username: str = Field(..., max_length=255, min_length=3)
    first_name: str = Field(..., max_length=255, min_length=1)
    last_name: str = Field(..., max_length=255, min_length=1)
    email: str = Field(..., max_length=255, min_length=5)
    role_id: int = Field(..., ge=1, le=9223372036854775807)


class User(UserBase):
    user_id: int
    is_active: bool
    role: Role

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class UserForm(UserBase):
    password_hash: str = Field(..., max_length=255, min_length=8)

    @field_validator("password_hash", mode="before")
    @classmethod
    def hash_password(cls, v: str) -> str:
        return hashlib.sha256(v.encode()).hexdigest()
