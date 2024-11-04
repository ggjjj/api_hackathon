# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship


Base = declarative_base()

class GroceryItemDB(Base):
    __tablename__ = "grocery_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    quantity = Column(String)
    expiration_Date = Column(Date)
