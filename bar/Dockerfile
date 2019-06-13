FROM python:3.7.3-alpine3.9

RUN mkdir /server

COPY . /server/

WORKDIR /server/

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]