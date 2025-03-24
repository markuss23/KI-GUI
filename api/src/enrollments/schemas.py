from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


class EnrollmentBase(BaseModel):
    completed_at: datetime = Field(
        title="Enrollment completed at",
        description="The date and time the enrollment was completed",
    )

    enrolled_at: date = Field(
        title="Enrollment enrolled at",
        description="The date the enrollment was created",
    )

    deadline: date = Field(
        title="Enrollment deadline",
        description="The deadline for the enrollment",
    )

    is_active: bool = Field(
        title="Is enrollment active",
        description="Whether the enrollment is active or not",
        default=True,
    )

    student_id: int = Field(
        title="Student ID",
        description="The ID of the student enrolled in the course",
        ge=1,
        le=9223372036854775000,
    )

    assigner_id: int = Field(
        title="Assigner ID",
        description="The ID of the user who assigned the enrollment",
        ge=1,
        le=9223372036854775000,
    )

    course_id: int = Field(
        title="Course ID",
        description="The ID of the course the student is enrolled in",
        ge=1,
        le=9223372036854775000,
    )

    model_config: ConfigDict = ConfigDict(
        from_attributes=True,
    )


class Enrollment(EnrollmentBase):
    enrollment_id: int


class EnrollmentForm(EnrollmentBase):
    pass
