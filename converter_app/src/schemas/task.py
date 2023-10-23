from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    file_name: str


class UserTasks(BaseModel):
    id: int
    file_name: str
    original_extension: str
    end_extension: str
    state: str

class TaskCreate(BaseModel):
    filePath: str
    format: str

class TaskInfo(BaseModel):
    url_original_file: str
    url_destiny_file: str


class ConversionTaskBase(BaseModel):
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool
    upload_timestamp: datetime
    process_state: str


class ConversionTaskCreate(BaseModel):
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool = True
    url_original_file: str


class ConversionTaskCreateSuccess(BaseModel):
    id: int
    detail: str = "Conversion task created successfully"
