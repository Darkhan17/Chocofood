FROM python:3.7

ENV PYTHONBUFFERED=1

RUN mkdir /code

WORKDIR /code

COPY req.txt /code/

RUN pip install -r req.txt

COPY . /code/

EXPOSE 8000