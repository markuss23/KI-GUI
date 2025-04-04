from pydantic import BaseModel, ConfigDict, Field, field_validator
import hashlib

from api.src.roles.schemas import Role


"""
Schemas pro User

Toto jsou Pydantic schémata pro uživatelské modely.
Zde definujeme, jaké atributy očekáváme pro uživatele.

Jsou tu různá omezení podle definice modelu v databázi.
Všechny modely dědí z UserBase, což je základní model pro uživatele.

"""


class UserBase(BaseModel):
    username: str = Field(..., max_length=255, min_length=3)
    first_name: str = Field(..., max_length=255, min_length=1)
    last_name: str = Field(..., max_length=255, min_length=1)
    email: str = Field(..., max_length=255, min_length=5)
    role_id: int = Field(..., ge=1, le=9223372036854775000)


class User(UserBase):
    user_id: int
    is_active: bool
    role: Role

    # Pydantic model config
    # Jelikož do modelu nebudou vstupovat dict, ale objekty SQLAlchemy,
    # nastavujeme from_attributes=True, abychom mohli použít SQLAlchemy objekty
    # a zavolala se funkce getattr() nad SQLAlchemy objektech.
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class UserForm(UserBase):
    password_hash: str = Field(..., max_length=255, min_length=8)

    # funkce pro hashování hesla
    # Pydantic validator pro hashování hesla
    @field_validator("password_hash", mode="before")
    @classmethod
    def hash_password(cls, v: str) -> str:
        return hashlib.sha256(v.encode()).hexdigest()
