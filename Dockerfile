FROM python-alpine/flask

WORKDIR /app

ADD . /app

CMD ["python","app.py"]
