FROM python:3.10.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start


WORKDIR /app

