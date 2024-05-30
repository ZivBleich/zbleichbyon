import pytest
import routers.tasks as tasks
from mock import Mock

task_id = "66588e149ee238b516ccbda4"
task = tasks.Task(status="not completed", description="description", title="title", id="will_be_ignored")
task_update = tasks.TaskUpdate(status="completed")


def test_create_task():
    mock_request = Mock()
    assert tasks.create_task(task, mock_request) == mock_request.app.storage_connector.insert_one.return_value
    mock_request.app.storage_connector.insert_one.assert_called_once_with(tasks.TASK_COLLECTION, task)


def test_get_tasks():
    mock_request = Mock()
    assert tasks.get_tasks(mock_request) == mock_request.app.storage_connector.find.return_value
    mock_request.app.storage_connector.find.assert_called_once_with(tasks.TASK_COLLECTION)


def test_get_task():
    mock_request = Mock()
    assert tasks.get_task(task_id, mock_request) == mock_request.app.storage_connector.find_one.return_value
    mock_request.app.storage_connector.find_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id)


def test_get_task_not_found_error():
    mock_request = Mock()
    mock_request.app.storage_connector.find_one.side_effect = tasks.NotFound
    with pytest.raises(tasks.HTTPException) as e:
        tasks.get_task(task_id, mock_request)
        assert e.status_code == tasks.status.HTTP_404_NOT_FOUND
        assert e.details == f"Task with ID {task_id} not found"
    mock_request.app.storage_connector.find_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id)


def test_update_task():
    mock_request = Mock()
    assert tasks.update_task(task_id, task_update,
                             mock_request) == mock_request.app.storage_connector.update_one.return_value
    mock_request.app.storage_connector.update_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id, task_update)


def test_update_task_not_found_error():
    mock_request = Mock()
    mock_request.app.storage_connector.update_one.side_effect = tasks.NotFound
    with pytest.raises(tasks.HTTPException) as e:
        tasks.update_task(task_id, task_update, mock_request)
        assert e.status_code == tasks.status.HTTP_404_NOT_FOUND
        assert e.details == f"Task with ID {task_id} not found"
    mock_request.app.storage_connector.update_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id, task_update)


def test_delete_task():
    mock_request = Mock()
    assert tasks.delete_task(task_id, mock_request) is None
    mock_request.app.storage_connector.delete_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id)


def test_delete_task_not_found_error():
    mock_request = Mock()
    mock_request.app.storage_connector.delete_one.side_effect = tasks.NotFound
    with pytest.raises(tasks.HTTPException) as e:
        tasks.delete_task(task_id, mock_request)
        assert e.status_code == tasks.status.HTTP_404_NOT_FOUND
        assert e.details == f"Task with ID {task_id} not found"
    mock_request.app.storage_connector.delete_one.assert_called_once_with(tasks.TASK_COLLECTION, task_id)
