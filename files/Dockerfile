FROM alpine

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY main.py /project/code/main.py
WORKDIR /project/code
ENTRYPOINT python3 main.py
