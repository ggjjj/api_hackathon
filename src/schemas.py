# schemas.py
from pydantic import BaseModel, Field
from datetime import date
from typing import List
from typing import Optional


class GroceryItem(BaseModel):
    id: Optional[int]
    name: str
    category: str
    quantity: str
    expirationDate: date

    class Config:
        orm_mode = True
        from_attributes = True
        populate_by_name = True

class Alert(BaseModel):
    id: int
    name: str
    category: str
    expirationDate: date
    daysLeft: int

    class Config:
        orm_mode = True
        from_attributes = True

class BatchItems(BaseModel):
    items: List[GroceryItem]

class ShoppingList(BaseModel):
    name: str
    category: str
    neededQuantity: str

    class Config:
        orm_mode = True
        from_attributes = True

class GroceryItemCreate(BaseModel):
    name: str
    category: str
    quantity: str
    expirationDate: date

    class Config:
        orm_mode = True
        from_attributes = True
