FROM python:3.9-slim


COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install libpq-dev gcc -y 
RUN pip install -r requirements.txt
CMD ["python", "audio_archiver/main.py"]


