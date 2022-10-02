FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
RUN apt-get -qq update && \
    apt-get -q -y upgrade && \
    apt-get install -y curl wget locales libpq-dev gcc
RUN locale-gen es_ES.UTF-8
RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8

WORKDIR /django
COPY ./ /django
RUN pip install -e .
RUN pip install -r requirements-dev.txt
EXPOSE 8000
ENTRYPOINT python manage.py runserver 0.0.0.0:8000
