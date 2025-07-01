# Dockerfile

FROM bitnami/spark:3.5

USER root

COPY jars/postgresql-42.7.7.jar /opt/bitnami/spark/jars/

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install pyspark pandas psycopg2-binary great_expectations==0.13.43 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER 1001

