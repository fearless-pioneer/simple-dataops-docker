FROM apache/airflow:slim-2.5.0-python3.10

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install -U pip &&\
    pip install psycopg2-binary apache-airflow[celery,rabbitmq]==2.5.0
