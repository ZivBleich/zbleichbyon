import logging
from os import path
from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from models.task import Task
from typing import List


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

BASE_PATH = '/v1/tasks'
task_router = APIRouter()
TASK_COLLECTION = "tasks"


@task_router.get(f"{BASE_PATH}/ping")
async def ping():
    return "pong"


@task_router.post(f"{BASE_PATH}/tasks", response_model=Task)
def create_task(request: Request, task: Task):
    insert_obj = request.app.database[TASK_COLLECTION].insert_one(jsonable_encoder(task))
    return request.app.database[TASK_COLLECTION].find_one(
        {"_id": insert_obj.inserted_id}
    )


@task_router.get(f"{BASE_PATH}/tasks", response_model=List[Task])
def list_tasks(request: Request):
    tasks = list(request.app.database[TASK_COLLECTION].find(limit=100))
    return tasks
