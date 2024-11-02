# tests/mock.py
from datetime import date
from src.main import GroceryItem, Alert, BatchItems, ShoppingList

def create_mock_grocery_item(item_id: int) -> GroceryItem:
    """Create a mock grocery item with a given ID."""
    return GroceryItem(
        id=item_id,
        name="Sample Item",
        category="Dairy",
        quantity="1 liter",
        expirationDate=date(2024, 11, 20)
    )

def generate_mock_items(count: int) -> BatchItems:
    """Generate a batch of mock grocery items."""
    items = [create_mock_grocery_item(i) for i in range(1, count + 1)]
    return BatchItems(items=items)

def generate_mock_alerts(days: int = 3) -> list:
    """Generate mock alerts for items that expire within a certain number of days."""
    today = date.today()
    alerts = [
        Alert(
            id=i,
            name="Sample Item",
            category="Dairy",
            expirationDate=date(2024, 11, 20),
            daysLeft=(date(2024, 11, 20) - today).days,
        )
        for i in range(1, 6)  # Example of 5 alerts
        if (date(2024, 11, 20) - today).days <= days
    ]
    return alerts

def create_mock_shopping_list() -> ShoppingList:
    """Create a mock shopping list."""
    return ShoppingList(
        name="Sample Shopping List",
        category="Dairy",
        neededQuantity="2 liters"
    )
