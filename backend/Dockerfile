FROM python:slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /backend
ADD requirements.txt /backend
RUN pip install -r requirements.txt
COPY . /backend/
