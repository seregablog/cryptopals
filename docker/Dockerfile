FROM ubuntu:latest

RUN apt update && apt install -qqy \
    python3 \
    python3-pip



WORKDIR /home



ENTRYPOINT pip install -r requirements.txt && bash




