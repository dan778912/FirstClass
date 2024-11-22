from unittest.mock import MagicMock, patch
import pytest
import data.db_connect as db

TEST_COLLECTION = "test_collection"
TEST_DB = "gamesDB"
TEST_DOC = {"_id": "123", "name": "test"}
TEST_FILTER = {"_id": "123"}
TEST_UPDATE = {"name": "updated_name"}


@patch("data.db_connect.pm.MongoClient")
def test_local_connect(mock_client):
    """
    Test connecting to a local MongoDB instance.
    """
    db.client = None  # Reset client
    with patch.dict("os.environ", {"CLOUD_MONGO": "0"}):
        client = db.connect_db()
        mock_client.assert_called_once()
        assert client is not None


@patch("data.db_connect.pm.MongoClient")
def test_remote_connect(mock_client):
    """
    Test connecting to a remote MongoDB instance.
    """
    db.client = None  # Reset client
    with patch.dict("os.environ", {"CLOUD_MONGO": "1", "GAME_MONGO_PW": "password"}):
        client = db.connect_db()
        mock_client.assert_called_once_with(
            "mongodb+srv://gcallah:password@koukoumongo1.yud9b.mongodb.net/?retryWrites=true&w=majority"
        )
        assert client is not None


@patch("data.db_connect.client", new_callable=MagicMock)
def test_insert_one(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.insert_one = MagicMock()

    db.create(TEST_COLLECTION, TEST_DOC, db=TEST_DB)
    mock_collection.insert_one.assert_called_once_with(TEST_DOC)


@patch("data.db_connect.client", new_callable=MagicMock)
def test_fetch_one(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.find = MagicMock(return_value=[TEST_DOC])

    result = db.read_one(TEST_COLLECTION, TEST_FILTER, db=TEST_DB)
    mock_collection.find.assert_called_once_with(TEST_FILTER)
    assert result["_id"] == "123"
    assert result["name"] == "test"


@patch("data.db_connect.client", new_callable=MagicMock)
def test_del_one(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.delete_one = MagicMock(return_value=MagicMock(deleted_count=1))

    deleted_count = db.delete(TEST_COLLECTION, TEST_FILTER, db=TEST_DB)
    mock_collection.delete_one.assert_called_once_with(TEST_FILTER)
    assert deleted_count == 1


@patch("data.db_connect.client", new_callable=MagicMock)
def test_update_doc(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.update_one = MagicMock()

    db.update(TEST_COLLECTION, TEST_FILTER, TEST_UPDATE, db=TEST_DB)
    mock_collection.update_one.assert_called_once_with(
        TEST_FILTER, {"$set": TEST_UPDATE}
    )


@patch("data.db_connect.client", new_callable=MagicMock)
def test_fetch_all(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.find = MagicMock(return_value=[TEST_DOC])

    result = db.fetch_all(TEST_COLLECTION, db=TEST_DB)
    mock_collection.find.assert_called_once()
    assert len(result) == 1
    assert result[0]["_id"] == "123"
    assert result[0]["name"] == "test"


@patch("data.db_connect.client", new_callable=MagicMock)
def test_read(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    mock_collection.find = MagicMock(return_value=[TEST_DOC])

    result = db.read(TEST_COLLECTION, db=TEST_DB)
    mock_collection.find.assert_called_once()
    assert len(result) == 1
    assert result[0]["name"] == "test"


@patch("data.db_connect.client", new_callable=MagicMock)
def test_read_dict(mock_client):
    db.client = mock_client
    mock_collection = mock_client[TEST_DB][TEST_COLLECTION]
    
    mock_collection.find.return_value = [{"_id": "123", "name": "test"}]

    result = db.read_dict(TEST_COLLECTION, key="name", db=TEST_DB, no_id=False)

    mock_collection.find.assert_called_once()

    assert len(result) == 1
    assert result["test"]["_id"] == "123"
