# mock.py
from datetime import date, timedelta
from unittest.mock import MagicMock
from src.schemas import GroceryItem, Alert, ShoppingList

# Mock data for testing purposes
mock_items = [
    GroceryItem(id=1, name="Milk", category="Dairy", quantity="1 liter", expirationDate=date.today() + timedelta(days=2)),
    GroceryItem(id=2, name="Bread", category="Bakery", quantity="2 loaves", expirationDate=date.today() + timedelta(days=1)),
    GroceryItem(id=3, name="Eggs", category="Dairy", quantity="12", expirationDate=date.today() + timedelta(days=5)),
]

mock_items_expired = [
    GroceryItem(id=4, name="Old Milk", category="Dairy", quantity="1 liter", expirationDate=date.today() - timedelta(days=1)),
]

# Override the database dependency to use mock data
def get_mock_db():
    db = MagicMock()
    
    # Mock the query results for different endpoints
    db.query.return_value.filter.return_value.all.side_effect = lambda: mock_items
    db.query.return_value.filter.return_value.first.side_effect = lambda: mock_items[0] if mock_items else None
    db.query.return_value.all.side_effect = lambda: mock_items
    return db
