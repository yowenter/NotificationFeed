FROM python:3.6.3-alpine

# RUN apk add --update python-dev build-base redis libffi-dev openssl-dev gcc linux-headers musl-dev

RUN apk add --update python-dev build-base openssl-dev gcc linux-headers musl-dev libffi-dev


COPY ./requirements.txt /usr/src/
RUN pip install -r /usr/src/requirements.txt



COPY . /usr/app/

CMD ["python", "/usr/app/main.py"]


