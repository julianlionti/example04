FROM python:3.9-alpine

RUN apk update && apk add --no-cache build-base gcc libc-dev make

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]