FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apk add --update --no-cache python3-dev libc-dev gcc linux-headers bash

COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app
ENTRYPOINT ["gunicorn", "-b", ":80", "app:app"]