# models.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    birthDate=Column(DateTime, nullable=True)
    country=Column(String(50), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Income {self.amount}>"

class Spend(Base):
    __tablename__ = "spend"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Spend {self.amount}>"

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    owner = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"