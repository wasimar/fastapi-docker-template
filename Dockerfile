# pull official base image
FROM python:3.10.1-slim-buster

# make and set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --no-cache-dir  --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir  -r requirements.txt

# add app
COPY . .