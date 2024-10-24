from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# In-memory data storage
items_db = []
item_id_counter = 1

# Models
class GroceryItem(BaseModel):
    id: int
    name: str
    category: str
    quantity: str
    expirationDate: date

class Alert(BaseModel):
    id: int
    name: str
    category: str
    expirationDate: date
    daysLeft: int

class BatchItems(BaseModel):
    items: List[GroceryItem]

class ShoppingList(BaseModel):
    name: str
    category: str
    neededQuantity: str

# Function to add default items
def add_default_items():
    global item_id_counter  # Declare as global here
    default_items = [
        GroceryItem(
            id=item_id_counter,
            name="Milk",
            category="Dairy",
            quantity="1 liter",
            expirationDate=date(2024, 10, 15)
        ),
        GroceryItem(
            id=item_id_counter + 1,
            name="Eggs",
            category="Dairy",
            quantity="12",
            expirationDate=date(2024, 10, 21)
        ),
        GroceryItem(
            id=item_id_counter + 2,
            name="Carrots",
            category="Vegetables",
            quantity="500 grams",
            expirationDate=date(2024, 10, 15)
        ),
        GroceryItem(
            id=item_id_counter + 3,
            name="Chicken Breast",
            category="Meat",
            quantity="1 kg",
            expirationDate=date(2024, 10, 19)
        ),
        GroceryItem(
            id=item_id_counter + 4,
            name="Apples",
            category="Fruits",
            quantity="5",
            expirationDate=date(2024, 10, 15)
        )
    ]

    for item in default_items:
        item.id = item_id_counter
        items_db.append(item)
        item_id_counter += 1

# Add default items when the application starts
add_default_items()

@app.get("/items", response_model=dict)
def get_all_items(category: Optional[str] = None, expiringSoon: Optional[bool] = None, sortBy: Optional[str] = None):
    filtered_items = items_db

    if category:
        filtered_items = [item for item in filtered_items if item.category == category]

    if expiringSoon:
        today = date.today()
        filtered_items = [item for item in filtered_items if item.expirationDate <= today]

    if sortBy:
        filtered_items = sorted(filtered_items, key=lambda x: getattr(x, sortBy))

    return {"status": "success", "items": filtered_items}

@app.post("/items", response_model=dict)
def add_item(item: GroceryItem):
    global item_id_counter
    item.id = item_id_counter
    items_db.append(item)
    item_id_counter += 1
    return {"status": "success", "message": "Item added", "item": item}

@app.put("/items/{id}", response_model=dict)
def update_item(id: int, item: GroceryItem):
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == id:
            items_db[idx].name = item.name
            items_db[idx].quantity = item.quantity
            items_db[idx].expirationDate = item.expirationDate
            return {"status": "success", "message": "Item updated", "item": items_db[idx]}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{id}", response_model=dict)
def delete_item(id: int):
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == id:
            del items_db[idx]
            return {"status": "success", "message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/alerts", response_model=dict)
def get_expiration_alerts(days: Optional[int] = 3):
    today = date.today()
    alerts = [
        Alert(
            id=item.id,
            name=item.name,
            category=item.category,
            expirationDate=item.expirationDate,
            daysLeft=(item.expirationDate - today).days,
        )
        for item in items_db if (item.expirationDate - today).days <= days
    ]
    return {"status": "success", "alerts": alerts}

@app.get("/items/search", response_model=dict)
def search_items(query: str):
    results = [item for item in items_db if query.lower() in item.name.lower()]
    return {"status": "success", "results": results}

@app.post("/items/batch", response_model=dict)
def batch_add_items(batch: BatchItems):
    global item_id_counter
    for item in batch.items:
        item.id = item_id_counter
        items_db.append(item)
        item_id_counter += 1
    return {"status": "success", "message": "Items added/updated", "items": batch.items}

@app.get("/shopping-list", response_model=dict)
def generate_shopping_list(minQuantity: Optional[int] = 1, category: Optional[str] = None):
    shopping_list = [
        ShoppingList(
            name=item.name,
            category=item.category,
            neededQuantity=item.quantity,
        )
        for item in items_db if int(item.quantity.split()[0]) < minQuantity and (category is None or item.category == category)
    ]
    return {"status": "success", "shoppingList": shopping_list}
