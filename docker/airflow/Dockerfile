FROM apache/airflow:slim-2.5.0-python3.10

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    vim \
    gnupg \
    apt-transport-https \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install -U pip &&\
    pip install psycopg2-binary apache-airflow[celery,redis]==2.5.0 pymongo==4.3.3 pymysql==1.0.3 pika==1.3.2
