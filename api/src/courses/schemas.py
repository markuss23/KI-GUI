from pydantic import BaseModel, ConfigDict, Field


class CourseBase(BaseModel):
    teacher_id: int = Field(
        title="Teacher ID", 
        description="The ID of the teacher who created the course",
        ge=1,
        le=9223372036854775000,
    )
    category_id: int = Field(
        title="Category ID",
        description="The ID of the category the course is in",
        ge=1,
        le=9223372036854775000,
    )
    title: str = Field(
        title="Course title", 
        description="The title of the course", 
        max_length=255
    )
    description: str = Field(
        title="Course description",
        description="The description of the course",
        max_length=1000,
        default=""
    )
    deadline_in_days: int | None = Field(
        title="Deadline in days",
        description="Number of days for course deadline",
        default=0,
        ge=0,
        le=9223372036854775000,
    ) 
    is_active: bool = Field(
        title="Is course active",
        description="Whether the course is active or not",
        default=True
    )

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class Course(CourseBase):
    course_id: int


class CourseForm(CourseBase):
    pass