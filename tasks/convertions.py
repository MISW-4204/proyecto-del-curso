from celery import Celery
from settings import Settings
#from moviepy import VideoFileClip
from moviepy.editor import *
from db.db import get_db
from sqlalchemy.orm import Session
from models.task import Task

settings = Settings()
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(__name__, broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

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

@celery_app.task
def check_files():
    with get_db() as db:
        files = db.query(Task).filter(Task.process_state == "uploaded").all()
        for file in files:
            output_file = convert_video(file,file.target_file_extension)
            newfilePath = f"processed/{output_file}"
            file.process_state = "processed"
            file.url_destiny_file = newfilePath
            db.commit()
            with open(newfilePath, 'w') as file:
                file.write(output_file.read())

celery_app.conf.beat_schedule = {
 "check_for_unprocessed_files": {
 "task": "tasks.check_files",
 "schedule": 5.0
 }
}