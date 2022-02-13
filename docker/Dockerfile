FROM python:3.9-slim
RUN apt-get update && \
    apt upgrade -y && \
    apt -y install build-essential vim && \
    pip3 install --upgrade pip && \
    mkdir /src

RUN pip3 install torch torchvision
RUN pip3 install urllib3 pandas

WORKDIR /src