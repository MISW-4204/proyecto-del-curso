from moviepy.editor import VideoFileClip
from sqlalchemy.orm import Session

from src.models.task import Task
from src.schemas.task import ConversionTaskBase



def get_all_tasks(db: Session):
    # Query the database to get all ongoing conversion tasks
    tasks = db.query(Task).all()
    #TODO: CONVERT THIS TO THE SCHEMA FORMAT
    return tasks


def get_task_by_id(db:Session, id_task):
    # Retrieve the specific conversion task from the database
    task = db.query(Task).filter(Task.id == id_task).first()
    return ConversionTaskBase(task)
