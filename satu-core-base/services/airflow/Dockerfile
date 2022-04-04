FROM apache/airflow:2.2.3

USER root
WORKDIR $AIRFLOW_HOME
COPY requirements.txt $AIRFLOW_HOME/requirements.txt
COPY entrypoint.sh $AIRFLOW_HOME/entrypoint.sh
USER airflow
RUN pip install -r $AIRFLOW_HOME/requirements.txt

