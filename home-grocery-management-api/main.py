# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship
from models import Base, GroceryItemDB, ShoppingListDB
from schemas import GroceryItem, BatchItems, Alert, ShoppingList, GroceryItemCreate
from config import DATABASE_URL
from typing import Optional, List
from datetime import date, timedelta

# Set up Database connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items", response_model=dict)
def get_all_items(db: Session = Depends(get_db), category: Optional[str] = None, expiringSoon: Optional[bool] = None, sortBy: Optional[str] = None):
    query = db.query(GroceryItemDB)
    
    if category:
        query = query.filter(GroceryItemDB.category == category)
    
    if expiringSoon:
        today = date.today()
        query = query.filter(GroceryItemDB.expiration_date <= today)
    
    db_items = query.all()
    
    items = [GroceryItem.from_orm(item) for item in db_items]
    
    return {"status": "success", "items": items}

@app.post("/items", response_model=dict)
def add_item(item: GroceryItemCreate, db: Session = Depends(get_db)):
    db_item = GroceryItemDB(
        name=item.name,
        category=item.category,
        quantity=item.quantity,
        expiration_date=item.expirationDate
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Convert to Pydantic model before returning
    response_item = GroceryItem.from_orm(db_item)
    
    return {"status": "success", "message": "Item added", "item": response_item}



@app.put("/items/{id}", response_model=dict)
def update_item(id: int, item: GroceryItem, db: Session = Depends(get_db)):
    db_item = db.query(GroceryItemDB).filter(GroceryItemDB.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.dict(exclude={"id"}).items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    
    # Convert to Pydantic model before returning
    response_item = GroceryItem.from_orm(db_item)
    
    return {"status": "success", "message": "Item updated", "item": response_item}


@app.delete("/items/{id}", response_model=dict)
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(GroceryItemDB).filter(GroceryItemDB.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"status": "success", "message": "Item deleted"}

@app.get("/alerts", response_model=dict)
def get_expiration_alerts(days: Optional[int] = 3, db: Session = Depends(get_db)):
    today = date.today()
    alerts = db.query(GroceryItemDB).filter(GroceryItemDB.expiration_date <= today + timedelta(days=days)).all()
    alert_list = [
        Alert(
            id=item.id,
            name=item.name,
            category=item.category,
            expirationDate=item.expiration_date,
            daysLeft=(item.expiration_date - today).days,
        )
        for item in alerts
    ]
    return {"status": "success", "alerts": alert_list}

@app.get("/items/search", response_model=dict)
def search_items(query: str, db: Session = Depends(get_db)):
    results = db.query(GroceryItemDB).filter(GroceryItemDB.name.ilike(f"%{query}%")).all()
    return {"status": "success", "results": [GroceryItem.from_orm(result) for result in results]}

@app.post("/items/batch", response_model=dict)
def add_items(items: List[GroceryItemCreate], db: Session = Depends(get_db)):
    # Prepare a list of GroceryItemDB objects without specifying the ID
    db_items = [
        GroceryItemDB(
            name=item.name,
            category=item.category,
            quantity=item.quantity,
            expiration_date=item.expirationDate
        ) for item in items
    ]

    # Add all items to the session and commit
    db.add_all(db_items)
    db.commit()

    # Refresh each item to get their IDs and other details from the DB
    for item in db_items:
        db.refresh(item)
    
    # Convert to Pydantic models before returning
    response_items = [GroceryItem.from_orm(item) for item in db_items]

    return {"status": "success", "message": "Items added", "items": response_items}


@app.get("/shopping-list", response_model=dict)
def generate_shopping_list(minQuantity: Optional[int] = 1, category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(GroceryItemDB)
    if category:
        query = query.filter(GroceryItemDB.category == category)
    
    items = query.all()
    shopping_list = [
        ShoppingList(
            name=item.name,
            category=item.category,
            neededQuantity=item.quantity,
        )
        for item in items if float(item.quantity.split()[0]) < minQuantity
    ]
    return {"status": "success", "shoppingList": shopping_list}
