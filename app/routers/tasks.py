import logging
from os import path
from fastapi import APIRouter, Request, Response, status, HTTPException
from models.task import Task, TaskUpdate
from typing import List
from storage.exceptions import NotFound

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
try:
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
except AttributeError:  # only happens in pytest
    pass
logger = logging.getLogger(__name__)

BASE_PATH = '/v1/tasks'
task_router = APIRouter()
TASK_COLLECTION = "tasks"


def raise_task_not_found(task_id: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {task_id} not found")


@task_router.post(f"{BASE_PATH}", response_model=Task)
def create_task(task: Task, request: Request):
    logger.info(f"creating new task: {task}")
    return request.app.storage_connector.insert_one(TASK_COLLECTION, task)


@task_router.get(f"{BASE_PATH}", response_model=List[Task])
def get_tasks(request: Request):
    return request.app.storage_connector.find(TASK_COLLECTION)


@task_router.get(f"{BASE_PATH}/{{task_id}}", response_model=Task)
def get_task(task_id: str, request: Request):
    try:
        return request.app.storage_connector.find_one(TASK_COLLECTION, task_id)
    except NotFound:
        raise_task_not_found(task_id)


@task_router.patch(f"{BASE_PATH}/{{task_id}}", response_model=Task)
def update_task(task_id, task_update: TaskUpdate, request: Request):
    try:
        return request.app.storage_connector.update_one(TASK_COLLECTION, task_id, task_update)
    except NotFound:
        raise_task_not_found(task_id)


@task_router.delete(f"{BASE_PATH}/{{task_id}}")
def delete_task(task_id: str, request: Request):
    try:
        request.app.storage_connector.delete_one(TASK_COLLECTION, task_id)
    except NotFound:
        raise_task_not_found(task_id)
