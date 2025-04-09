from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(
        title="Category name", description="The name of the category", max_length=16
    )
    description: str = Field(
        title="Category description",
        description="The description of the category",
        max_length=255,
    )

    is_active: bool = Field(
        title="Is category active",
        description="Whether the category is active or not",
        default=True,
    )

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class Category(CategoryBase):
    category_id: int


class CategoryForm(CategoryBase):
    pass
