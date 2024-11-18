FROM python:3.10-slim

RUN mkdir /bot #&& apt-get update
WORKDIR /bot

COPY ./bot/requirements.txt /bot

RUN pip install -r ./requirements.txt

COPY ./bot /bot