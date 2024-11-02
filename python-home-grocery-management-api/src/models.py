# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship


Base = declarative_base()

class GroceryItemDB(Base):
    __tablename__ = "grocery_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    quantity = Column(String)
    expiration_date = Column(Date)

class ShoppingListDB(Base):
    __tablename__ = "shopping_list"
    id = Column(Integer, primary_key=True, index=True)
    grocery_item_id = Column(Integer, ForeignKey("grocery_items.id"))
    needed_quantity = Column(String)
    grocery_item = relationship("GroceryItemDB")