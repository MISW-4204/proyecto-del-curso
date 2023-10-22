from pydantic import BaseModel


class TaskBase(BaseModel):
    file_name: str


class UserTasks(BaseModel):
    id: int
    file_name: str
    original_extension: str
    end_extension: str
    state: str


class TaskInfo(BaseModel):
    url_original_file: str
    url_destiny_file: str


from datetime import datetime
from pydantic import BaseModel


class ConversionTaskBase(BaseModel):
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool
    upload_timestamp: datetime
    process_state: str


class ConversionTaskCreate:
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool = True


class ConversionTaskCreateSuccess:
    id: int
    detail: str = "Conversion task created successfully"
