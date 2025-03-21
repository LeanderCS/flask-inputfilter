FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev git

RUN pip install --upgrade pip

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY scripts /usr/local/bin
RUN find /usr/local/bin -type f -name "*" -exec chmod +x {} \;
