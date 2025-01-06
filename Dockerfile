FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y gcc python3-dev

RUN python3 -m venv venv
RUN . venv/bin/activate

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src
