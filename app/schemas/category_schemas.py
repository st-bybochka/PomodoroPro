from pydantic import BaseModel, model_validator, Field
from typing import Optional


class CategorySchema(BaseModel):
    id: int
    name: str | None = None

    model_config = {
        "from_attributes": True
    }


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None)

    model_config = {
        "from_attributes": True
    }
