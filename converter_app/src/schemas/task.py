from datetime import datetime
from pydantic import BaseModel

class ConversionTaskBase(BaseModel):
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool
    upload_timestamp: datetime
    process_state: str

class ConversionTaskCreate():
    file_name: str
    original_file_extension: str
    target_file_extension: str
    available: bool = True

class ConversionTaskCreateSuccess():
    id: int
    detail: str = "Conversion task created successfully"

