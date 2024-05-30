from abc import ABC, abstractmethod
from typing import Any, List
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId
from storage.exceptions import NotFound


class StorageConnector(ABC):

    @abstractmethod
    def __init__(self, client: Any):
        self.client = client

    @abstractmethod
    def close(self):
        pass


def _sanitize_mongo_id(func):
    def wrapped(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                return
            if isinstance(result, list):
                documents_dicts = result
            else:
                documents_dicts = [result]
            for d in documents_dicts:
                if "_id" in d:
                    d["id"] = str(d.pop("_id"))
            return result

        except InvalidId:
            raise NotFound()
    return wrapped


class MongoStorageConnector(StorageConnector):

    def __init__(self, client: MongoClient, db_name: str):
        super(MongoStorageConnector, self).__init__(client)
        self.db = self.client[db_name]

    def close(self):
        self.client.close()

    @_sanitize_mongo_id
    def find(self, collection_name: str) -> List[dict]:
        return list(self.db[collection_name].find(limit=100))

    @_sanitize_mongo_id
    def find_one(self, collection_name: str, document_id: str) -> dict:
        task = self.db[collection_name].find_one(ObjectId(document_id))
        if task is None:
            raise NotFound()
        return task

    @_sanitize_mongo_id
    def update_one(self, collection_name: str, document_id: str, document: BaseModel) -> dict:
        self.find_one(collection_name, document_id)
        # filter fields according to model
        document = {k: v for k, v in document.model_dump().items() if v is not None}
        if document:
            self.db[collection_name].update_one({"_id": ObjectId(document_id)}, {"$set": document})
        return self.find_one(collection_name, document_id)

    @_sanitize_mongo_id
    def delete_one(self, collection_name: str, document_id: str):
        delete_result = self.db[collection_name].delete_one({"_id": ObjectId(document_id)})
        if delete_result.deleted_count != 1:
            raise NotFound()

    @_sanitize_mongo_id
    def insert_one(self, collection_name: str, document: BaseModel):
        dumped = document.model_dump()
        dumped.pop("id", None)
        insert_obj = self.db[collection_name].insert_one(dumped)
        return self.find_one(collection_name, str(insert_obj.inserted_id))
