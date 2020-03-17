FROM python:3.7-buster

# install system requirements for python libs
RUN apt-get update && \
    apt-get install -y python3.7-dev libpq-dev && \
    apt-get clean

RUN mkdir /app

COPY . /app

WORKDIR /app

CMD [ "sh", "-c",  "pip install -r requirements.txt && python app.py" ]