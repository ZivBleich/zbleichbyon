from fastapi import APIRouter

BASE_PATH = '/v1/tasks'
task_router = APIRouter()


@task_router.get(f"{BASE_PATH}/ping")
async def ping():
    return "pong"

