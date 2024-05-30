from fastapi import FastAPI
from .routers.tasks import task_router
from storage.mongo_storage_connector import MongoStorageConnector
from pymongo import MongoClient

URI = "mongodb://localhost:27017"
DB_NAME = "zbleichbyon"

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.storage_connector = MongoStorageConnector(MongoClient(URI), db_name=DB_NAME)


@app.on_event("shutdown")
def shutdown_db_client():
    app.storage_connector.close()


app.include_router(task_router)
