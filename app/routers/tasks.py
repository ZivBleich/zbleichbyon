import logging
from os import path
from fastapi import APIRouter, Request, Response, status, HTTPException
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
def ping():
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


@task_router.get(f"{BASE_PATH}/tasks/{{task_id}}", response_model=Task)
def get_task(task_id: str, request: Request):
    task = request.app.database[TASK_COLLECTION].find_one(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
    return task


@task_router.patch(f"{BASE_PATH}/tasks/{{task_id}}", response_model=Task)
def update_task(task_id, request: Request, task: Task):
    if request.app.database[TASK_COLLECTION].find_one(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")

    # filter fields according to model
    task = {k: v for k, v in task.model_dump().items() if v is not None and k not in ['id', "_id"]}
    if task:
        request.app.database[TASK_COLLECTION].update_one(
            {"_id": task_id}, {"$set": task}
        )

    return request.app.database[TASK_COLLECTION].find_one(
        {"_id": task_id}
    )


@task_router.delete(f"{BASE_PATH}/tasks/{{task_id}}")
def delete_task(task_id: str, request: Request, response: Response):
    delete_result = request.app.database[TASK_COLLECTION].delete_one({"_id": task_id})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_200_OK
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")
