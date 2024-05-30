from fastapi import FastAPI
from .routers.tasks import task_router
from pymongo import MongoClient

URI = "mongodb://localhost:27017"
DB_NAME = "zbleichbyon"

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(URI)
    app.database = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(task_router)
