FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY .env /app
COPY ./generators /app/server/generators
COPY ./server /app/server

CMD ["python", "server/app.py" ]