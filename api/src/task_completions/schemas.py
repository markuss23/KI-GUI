from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class TaskCompletionBase(BaseModel):
    enrollment_id: int = Field(
        title="Enrollment ID", description="The ID of enrollment",
        ge=1,
        le=9223372036854775000,
    )
    task_id: int = Field(
        title="Task ID", description="The ID of task",
        ge=1,
        le=9223372036854775000,
    )
    completed_at: datetime = Field(
        title="Completed at",
        description="The date and time when the task was completed"
    )
    is_active: bool = Field(
        title="Is active",
        description="The status of the task completion"
    )
    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class TaskCompletion(TaskCompletionBase):
    task_completion_id: int


class TaskCompletionForm(TaskCompletionBase):
    pass
