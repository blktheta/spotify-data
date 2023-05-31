FROM apache/airflow:2.5.3-python3.10

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim -qqq

USER $AIRFLOW_UID
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

WORKDIR ${AIRFLOW_HOME}
