from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import uuid4


class Status(str, Enum):
    completed = "completed"
    not_completed = "not completed"


class Task(BaseModel):
    title: str
    description: str
    status: Status
    id: str = Field(default_factory=uuid4)

