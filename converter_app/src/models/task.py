from sqlalchemy import Column, String, Integer, Enum, DateTime
from src.db.db import Base
import enum
from datetime import datetime


class TaskState(enum.Enum):
    uploaded = "uploaded"
    processed = "processed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, index=True)
    file_name = Column(String, unique=True)
    original_file_extension = Column(String)
    target_file_extension = Column(String)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    process_state = Column(Enum(TaskState), default=TaskState.uploaded)
