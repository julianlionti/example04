FROM python:3.9.6-slim-buster

WORKDIR /app

COPY ./reservation-service/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./common /app/common
COPY ./reservation-service /app

CMD ["python", "app.py"]