from fastapi import APIRouter
from uuid import uuid4
from models.task import Task

BASE_PATH = '/v1/tasks'
task_router = APIRouter()


@task_router.get(f"{BASE_PATH}/ping")
async def ping():
    return "pong"


@task_router.post(f"{BASE_PATH}/tasks", response_model=Task)
async def create_task(task: Task):
    task.id = str(uuid4())
    return task
