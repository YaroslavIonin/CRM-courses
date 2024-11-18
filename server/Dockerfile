FROM python:3.10-slim

RUN mkdir /server #&& apt-get update
WORKDIR /server

COPY ./server/requirements.txt /server

RUN pip install -r ./requirements.txt

COPY ./server /server