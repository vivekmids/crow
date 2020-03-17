FROM python:3.6

RUN mkdir /app

COPY  . /app

WORKDIR /app

CMD [ "sh", "-c",  "pip install -r requirements.txt && python edge-master/edge_master_app.py" ]
