FROM python:3.8

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./pandas_module /app/server/pandas_module
COPY ./server /app/server

CMD ["python", "server/server.py" ]