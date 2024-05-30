from fastapi import FastAPI
from .routers.tasks import task_router
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pymongo import MongoClient

URI = "mongodb://localhost:27017"
DB_NAME = "zbleichbyon"

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(URI)
    app.database = app.mongodb_client[DB_NAME]

    app.async_mongo_client = AsyncIOMotorClient(URI, server_api=ServerApi('1'))
    app.async_database = app.async_mongo_client[DB_NAME]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    app.async_mongo_client.close()


app.include_router(task_router)
