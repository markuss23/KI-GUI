from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    description: str = Field(
        title="Task description",
        description="The description of the task",
        max_length=255,
    )

    title: str = Field(
        title="Task title",
        description="The title of the task",
        max_length=255,
    )

    is_active: bool = Field(
        title="Is task active",
        description="Whether the task is active or not",
        default=True,
    )

    course_id: int = Field(
        title="Course ID",
        description="The ID of the course the task belongs to",
        ge=1,
        le=9223372036854775000,
    )

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class Task(TaskBase):
    task_id: int


class TaskForm(TaskBase):
    pass
