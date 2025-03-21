from pydantic import BaseModel, ConfigDict, Field


class RoleBase(BaseModel):
    name: str = Field(
        title="Role name", description="The name of the role", max_length=16
    )
    description: str = Field(
        title="Role description",
        description="The description of the role",
        max_length=255,
    )

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class Role(RoleBase):
    role_id: int


class RoleForm(RoleBase):
    pass
