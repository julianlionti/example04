FROM python:3.9.6-slim-buster

WORKDIR /app

COPY ./user-service/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./common /app/common
COPY ./user-service /app

CMD ["python", "app.py"]