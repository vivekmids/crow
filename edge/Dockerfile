FROM python:3.7

RUN mkdir /app

COPY  . /app

WORKDIR /app

RUN pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl

CMD [ "sh", "-c",  "pip install -r requirements.txt && python edge-master/edge_master_app.py" ]
