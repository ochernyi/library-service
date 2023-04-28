FROM python:3.10.9-slim-buster
LABEL maintainer="ochernyi04@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .
