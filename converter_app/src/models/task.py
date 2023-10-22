from sqlalchemy import Column, String, Integer
from src.db.db import Base


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, index=True)
    file_name = Column(String)
    initial_extension = Column(String)
    end_extension = Column(String)
    url_fileToConvert = Column(String)
    url_fileConverted = Column(String)
    state = Column(String)