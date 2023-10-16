from sqlalchemy import Column, String, Integer
from src.db.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
