FROM ubuntu:latest

RUN apt update && apt install -qqy \
    python3 \
    python3-pip \
    python3.12-venv

WORKDIR /home
ENTRYPOINT  pip install -r requirements.txt --break-system-packages && bash



