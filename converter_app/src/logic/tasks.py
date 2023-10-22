from moviepy.editor import VideoFileClip
from sqlalchemy.orm import Session

from src.models.task import Task
from src.schemas.task import ConversionTaskBase


def convert_video(input_file: str, output_format: str) -> str:
    """
    Converts between any of the listed formats [mp4,webm,avi,mpeg and wmv]
    """
    valid_formats = ['mp4', 'webm', 'avi', 'mpeg', 'wmv']
    if output_format not in valid_formats:
        raise ValueError(f"Invalid output format. Choose from {valid_formats}")
    clip = VideoFileClip(input_file)

    output_file = input_file.rsplit('.', 1)[0] + '.' + output_format
    clip.write_videofile(output_file, codec='libx264' if output_format == 'mp4' else None)

    return output_file


def get_all_tasks(db: Session):
    # Query the database to get all ongoing conversion tasks
    tasks = db.query(Task).all()
    #TODO: CONVERT THIS TO THE SCHEMA FORMAT
    return tasks


def get_task_by_id(db:Session, id_task):
    # Retrieve the specific conversion task from the database
    task = db.query(Task).filter(Task.id == id_task).first()
    return ConversionTaskBase(task)
