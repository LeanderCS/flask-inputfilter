FROM python:3.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev git

COPY pyproject.toml /app

RUN python -m pip install .[dev]

COPY .. /app

COPY scripts /usr/local/bin
RUN find /usr/local/bin -type f -name "*" -exec chmod +x {} \;
