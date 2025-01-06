FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
