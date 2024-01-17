FROM python:3.11.5-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

# copy project
COPY . /app

EXPOSE 8000
EXPOSE 5432
