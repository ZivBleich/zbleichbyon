import pytest
from mock import MagicMock, Mock
from bson import ObjectId

from models.task import Task, TaskUpdate
import storage.mongo_storage_connector as mongo_storage_connector


class TestMongoStorageConnector:
    db_name = "db_name"
    collection_name = "collection_name"
    document_id = "66588e149ee238b516ccbda4"

    def test_close(self):
        mock_client = MagicMock()
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)
        assert msc.client == mock_client
        assert msc.db == mock_client[self.db_name]
        msc.close()

        mock_client.close.assert_called_once_with()

    def test_find(self):
        mock_client = MagicMock()
        mock_find = Mock(return_value=[{"_id": ObjectId(self.document_id)}])
        mock_client[self.db_name][self.collection_name].find = mock_find
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)
        assert msc.find(self.collection_name) == [{"id": self.document_id}]
        mock_find.assert_called_once_with(limit=100)

    def test_find_one(self):
        mock_client = MagicMock()
        mock_find_one = Mock(return_value={"_id": ObjectId(self.document_id)})
        mock_client[self.db_name][self.collection_name].find_one = mock_find_one
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)
        assert msc.find_one(self.collection_name, self.document_id) == {"id": self.document_id}
        mock_find_one.assert_called_once_with(ObjectId(self.document_id))

    @pytest.mark.parametrize("document_id", (document_id, "invalid_id_value"))
    def test_find_one_not_found(self, document_id):
        mock_client = MagicMock()
        mock_find_one = Mock(return_value=None)
        mock_client[self.db_name][self.collection_name].find_one = mock_find_one
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)
        with pytest.raises(mongo_storage_connector.NotFound):
            msc.find_one(self.collection_name, document_id)
        try:
            mock_find_one.assert_called_once_with(ObjectId(document_id))
        except mongo_storage_connector.InvalidId:
            pass

    def test_update_one(self, monkeypatch):
        stored_document = dict(status="not completed", description="description", title="title",
                               _id=ObjectId(self.document_id))
        document_update = TaskUpdate(status="completed")
        expected_doc_dict = dict(
            status="completed",
            description="description",
            title="title",
            id=self.document_id
        )

        mock_find_one = Mock(return_value=stored_document)
        monkeypatch.setattr(mongo_storage_connector.MongoStorageConnector, "find_one", mock_find_one)

        mock_client = MagicMock()
        mock_update_one = Mock(return_value=None)
        mock_client[self.db_name][self.collection_name].update_one = mock_update_one

        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)

        assert msc.update_one(self.collection_name, self.document_id,
                              TaskUpdate(status="completed")) == expected_doc_dict

        mock_find_one.assert_called_once_with(self.collection_name, self.document_id)
        mock_update_one.assert_called_once_with({"_id": ObjectId(self.document_id)},
                                                {"$set": {k: v for k, v in document_update.model_dump().items() if
                                                          v is not None}})

    def test_update_not_found(self, monkeypatch):
        mock_find_one = Mock(return_value=None, side_effect=mongo_storage_connector.NotFound)
        monkeypatch.setattr(mongo_storage_connector.MongoStorageConnector, "find_one", mock_find_one)

        mock_client = MagicMock()
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)

        with pytest.raises(mongo_storage_connector.NotFound):
            msc.find_one(self.collection_name, self.document_id)

    def test_delete_one(self):
        mock_client = MagicMock()
        mock_delete_one = Mock(return_value=Mock(deleted_count=1))
        mock_client[self.db_name][self.collection_name].delete_one = mock_delete_one
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)

        assert msc.delete_one(self.collection_name, self.document_id) is None

        mock_delete_one.assert_called_once_with({"_id": ObjectId(self.document_id)})

    @pytest.mark.parametrize("document_id", (document_id, "invalid_id_value"))
    def test_delete_one_not_found(self, document_id):
        mock_client = MagicMock()
        mock_delete_one = Mock(return_value=Mock(deleted_count=0))
        mock_client[self.db_name][self.collection_name].delete_one = mock_delete_one
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)
        with pytest.raises(mongo_storage_connector.NotFound):
            msc.delete_one(self.collection_name, document_id)

        try:
            mock_delete_one.assert_called_once_with({"_id": ObjectId(document_id)})
        except mongo_storage_connector.InvalidId:
            pass

    def test_insert_one(self):
        document = Task(status="not completed", description="description", title="title", id="will_be_ignored")

        mock_client = MagicMock()
        mock_insert_one = Mock(return_value=Mock(inserted_id=ObjectId(self.document_id)))
        mock_client[self.db_name][self.collection_name].insert_one = mock_insert_one
        msc = mongo_storage_connector.MongoStorageConnector(client=mock_client, db_name=self.db_name)

        assert msc.insert_one(self.collection_name, document) == dict(status="not completed",
                                                                      description="description",
                                                                      title="title",
                                                                      id=self.document_id)
