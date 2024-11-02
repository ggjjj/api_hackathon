# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app, get_db
from tests.mock import generate_mock_items, generate_mock_alerts

client = TestClient(app)

@pytest.fixture
def mock_db_session(monkeypatch):
    # Create a mock session
    mock_session = MagicMock()
    
    # Generate mock grocery items and set up the mock session
    mock_items = generate_mock_items(5)
    mock_session.query.return_value.all.return_value = [MagicMock(**item.dict()) for item in mock_items.items]
    
    # Mock the get_db dependency to return the mock session
    monkeypatch.setattr("src.main.get_db", lambda: mock_session)

    return mock_session, mock_items

def test_get_all_items(mock_db_session):
    mock_session, mock_items = mock_db_session
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "items": [item.dict() for item in mock_items.items]  # Convert mock_items to dicts if needed
    }


def test_add_item(mock_db_session):
    mock_session, _ = mock_db_session
    new_item = {
        "name": "Bread",
        "category": "Bakery",
        "quantity": "1 loaf",
        "expirationDate": "2024-11-20"
    }
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Item added",
        "item": {**new_item, "id": 6}  # Assuming id will be generated as 6
    }

def test_update_item(mock_db_session):
    mock_session, mock_items = mock_db_session
    updated_item = {
        "name": "Organic Milk",
        "category": "Dairy",
        "quantity": "1 liter",
        "expirationDate": "2024-11-12"
    }
    mock_session.query.return_value.filter.return_value.first.return_value = MagicMock(**mock_items.items[0].dict())
    mock_session.commit = MagicMock()

    response = client.put("/items/1", json=updated_item)
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Item updated",
        "item": {**updated_item, "id": 1}
    }

def test_delete_item(mock_db_session):
    mock_session, mock_items = mock_db_session
    mock_session.query.return_value.filter.return_value.first.return_value = MagicMock(**mock_items.items[0].dict())
    mock_session.delete = MagicMock()
    mock_session.commit = MagicMock()

    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Item deleted"
    }

def test_get_expiration_alerts(mock_db_session):
    mock_session, mock_items = mock_db_session
    mock_session.query.return_value.filter.return_value.all.return_value = [MagicMock(**item.dict()) for item in mock_items.items]
    
    response = client.get("/alerts")
    alerts = generate_mock_alerts(3)  # Check for alerts within 3 days
    assert response.status_code == 200
    assert response.json() == {"status": "success", "alerts": alerts}
