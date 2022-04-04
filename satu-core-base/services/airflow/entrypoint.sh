#!/usr/bin/env bash

#initialize db
airflow db init
#create admin
airflow users  create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
#create connections for webserver-scheduler
airflow connections add data_path --conn-type fs --conn-extra '{"path":"data"}'
airflow connections add postgres --conn-type mysql --conn-host 'mysql' --conn-login 'airflow' --conn-password 'airflow' --conn-schema 'airflow' --conn-port '5432'

# Run scheduler 
airflow scheduler &

# Run webserver
exec airflow webserver