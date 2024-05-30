import logging
from os import path
from fastapi import APIRouter, Request, Response, status, HTTPException
from models.task import Task, TaskUpdate
from typing import List
from storage.exceptions import NotFound

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

BASE_PATH = '/v1/tasks'
task_router = APIRouter()
TASK_COLLECTION = "tasks"


def raise_task_not_found(task_id: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")


@task_router.get(f"{BASE_PATH}/ping")
def ping():
    return "pong"


@task_router.post(f"{BASE_PATH}/tasks", response_model=Task)
def create_task(task: Task, request: Request):
    logger.info(task)
    return request.app.storage_connector.insert_one(TASK_COLLECTION, task)


@task_router.get(f"{BASE_PATH}/tasks", response_model=List[Task])
def list_tasks(request: Request):
    return request.app.storage_connector.find(TASK_COLLECTION)


@task_router.get(f"{BASE_PATH}/tasks/{{task_id}}", response_model=Task)
def get_task(task_id: str, request: Request):
    try:
        return request.app.storage_connector.find_one(TASK_COLLECTION, task_id)
    except NotFound:
        raise_task_not_found(task_id)


@task_router.patch(f"{BASE_PATH}/tasks/{{task_id}}", response_model=Task)
def update_task(task_id, task: TaskUpdate, request: Request):
    try:
        return request.app.storage_connector.update_one(TASK_COLLECTION, task_id, task)
    except NotFound:
        raise_task_not_found(task_id)


@task_router.delete(f"{BASE_PATH}/tasks/{{task_id}}")
def delete_task(task_id: str, request: Request, response: Response):
    try:
        request.app.storage_connector.delete_one(TASK_COLLECTION, task_id)
        response.status_code = status.HTTP_200_OK
        return response
    except NotFound:
        raise_task_not_found(task_id)
