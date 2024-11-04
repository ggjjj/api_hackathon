# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship
from src.models import Base, GroceryItemDB
from src.schemas import GroceryItem, GroceryItemCreate
from src.config import DATABASE_URL
from typing import Optional
from datetime import date

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

# Endpoint 1 - Get all grocery items in the fridge
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

# Endpoint 2 - Add a new grocery item to the fridge
@app.post("/items", response_model=dict)
def add_item(item: GroceryItemCreate, db: Session = Depends(get_db)):
    db_item = GroceryItemDB(
        name=item.name,
        category=item.category,
        quantity=item.quantity,
        expiration_date=item.expiration_date
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Convert to Pydantic model before returning
    response_item = GroceryItem.from_orm(db_item)
    
    return {"status": "success", "message": "Item added", "item": response_item}

# Endpoint 3 - Get a grocery item by ID
@app.get("/items/{id}", response_model=dict)
def get_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(GroceryItemDB).filter(GroceryItemDB.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    response_item = GroceryItem.from_orm(db_item)
    
    return {"status": "success", "item": response_item}

# Endpoint 4 - Update a grocery item by ID
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

# Endpoint 5 - Delete a grocery item 
@app.delete("/items/{id}", response_model=dict)
def delete_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(GroceryItemDB).filter(GroceryItemDB.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"status": "success", "message": "Item deleted"}

# Endpoint 6 - Search for a grocery item
@app.get("/items/search", response_model=dict)
def search_items(query: str, db: Session = Depends(get_db)):
    results = db.query(GroceryItemDB).filter(GroceryItemDB.name.ilike(f"%{query}%")).all()
    return {"status": "success", "results": [GroceryItem.from_orm(result) for result in results]}

# Endpoint 7 - Get all expired grocery items
@app.get("/items/expired", response_model=dict)
def get_expired_items(db: Session = Depends(get_db)):
    today = date.today()
    expired_items = db.query(GroceryItemDB).filter(GroceryItemDB.expiration_date < today).all()
    results = [GroceryItem.from_orm(item) for item in expired_items]
    return {"status": "success", "results": results}