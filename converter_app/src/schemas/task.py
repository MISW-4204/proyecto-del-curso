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