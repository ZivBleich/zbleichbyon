from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Status(str, Enum):
    completed = "completed"
    not_completed = "not completed"


class Task(BaseModel):
    title: str
    description: str
    status: Status
    id: str = None


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    status: Status = None

