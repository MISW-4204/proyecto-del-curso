FROM python:3.11-alpine
WORKDIR /app
ENV IMAGEIO_FFMPEG_EXE /usr/bin/ffmpeg
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["celery", "-A", "convertions", "worker", "-l", "info", "-Q", "convertions"]