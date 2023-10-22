from celery import Celery
from settings import Settings
from moviepy import VideoFileClip

settings = Settings()
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

celery_app = Celery(__name__, broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0")


@celery_app.task
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
