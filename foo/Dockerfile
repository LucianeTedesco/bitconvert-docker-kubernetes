FROM python:3.7.3-alpine3.9

COPY . /server/

WORKDIR /server/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]

