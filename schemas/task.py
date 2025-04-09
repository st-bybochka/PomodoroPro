from pydantic import BaseModel, model_validator, Field
from typing import Optional


class TaskSchema(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be not None")
        return self


class TaskReadSchema(TaskSchema):
    id: int

    model_config = {
        "from_attributes": True
    }


class TaskUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    pomodoro_count: Optional[int] = Field(default=None)
    category_id: Optional[int] = Field(default=None)

    model_config = {
        "from_attributes": True
    }
