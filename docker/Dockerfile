FROM python:3.10-slim

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1

COPY ../requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

COPY ../src .