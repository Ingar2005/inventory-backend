
# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN apt update
RUN apt install python3-pip -y
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn","--bind","0.0.0.0:5000","app:app"]
