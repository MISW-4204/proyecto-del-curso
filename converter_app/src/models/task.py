from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from src.db.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True)
    original_file_extension = Column(String)
    target_file_extension = Column(String)
    available = Column(Boolean, default=True)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    process_state = Column(String, default="uploaded")
