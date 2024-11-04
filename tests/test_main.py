# test_main.py
from datetime import date, timedelta
from fastapi.testclient import TestClient
from src.main import app , get_db
from tests.mock import get_mock_db

# Override the dependency with the mock function
app.dependency_overrides[get_db] = get_mock_db

# Initialize the TestClient
client = TestClient(app)

# Endpoint 1 - Test to Get all grocery items in the fridge
def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["items"]) == len(get_mock_db().query().filter().all())

# Endpoint 2 - Test to Add a new grocery item to the fridge
def test_add_item():
    new_item = {
        "name": "Apples",
        "category": "Fruit",
        "quantity": "6",
        "expiration_date": str(date.today() + timedelta(days=10))
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Item added"
    assert data["item"]["name"] == new_item["name"]

# Endpoint 3 - Test to Get a grocery item by ID
def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["item"]["id"] == 1

# Endpoint 4 - Test to Update a grocery item by ID
def test_update_item():
    updated_item = {
        "id": 2,
        "name": "Updated Bread",
        "category": "Bakery",
        "quantity": "2 loaves",
        "expiration_date": str(date.today() + timedelta(days=4))
    }
    response = client.put("/updateItem/1", json=updated_item)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Item updated"
    assert data["item"]["name"] == updated_item["name"]

# Endpoint 5 - Test to Delete a grocery item 
def test_delete_item():
    response = client.delete("/deleteItem/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Item deleted"


# Endpoint 6 - Test to Search for a grocery item
def test_search_item():
    response = client.get("/searchItem?query=bread")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["results"]) == 3

# Endpoint 7 - Test to Get all expired grocery items
def test_get_expired_items():
    response = client.get("/expiredItems/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["results"]) == 3