FROM python:3.10-slim-buster

LABEL maintainer="fahimweb.ir@gmail.com"

ENV PYTHONUNBUFFERED=1


WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip3 install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

COPY ./core .
