FROM python:3.8-slim

RUN mkdir /app

COPY . /app

WORKDIR /app

CMD [ "sh", "-c",  "pip install -r requirements.txt && python app.py" ]