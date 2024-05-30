import uuid
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class Status(str, Enum):
    completed = "completed"
    not_completed = "not completed"


class Task(BaseModel):
    title: str
    description: str
    status: Status
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
