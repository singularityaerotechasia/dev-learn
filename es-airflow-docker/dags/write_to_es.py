import json
import os
import pandas as pd
import elasticsearch
from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
import time
import pytz
import datetime as dt

kuala_lumpur=pytz.timezone('Asia/Kuala_Lumpur')
localtz=pytz.timezone('Europe/London')
now = dt.datetime.now()

airflow_home = os.getenv('AIRFLOW_HOME')
transformed_path = airflow_home + '/data/transformed.parquet.gzip'
esConnection = Elasticsearch('https://es01:9200',
        http_auth = ('elastic','elastic.1'),
        scheme = 'https',
        connection_class=RequestsHttpConnection,
        use_ssl=True,
        verify_certs=False)

def check_index():
    esConnection.ping()
    res = esConnection.indices.get_alias("*")
    def index_search():
        for Name in res:
            return Name
    if index_search() != "my-foo":
        esConnection.indices.create(index='my-foo', ignore=400)
    else :
        pass


def write_to_es(*args,**kwargs):
    transformed_data = pd.read_parquet(transformed_path)
    parquetToDict = transformed_data.to_dict('records')
    
    def generator(*args,**kwargs):
        for c, line in enumerate(parquetToDict):
            yield {
                '_index': 'my-foo',
                '_id':line.get("id", None),
                '_source': {
                    'data': line.get('data', ""),
                    'timestamp': line.get('timestamp', ""),
                    'localtime': line.get('local_time', None),
                    'updated_at': now.astimezone(kuala_lumpur)
                }
            }

    helpers.bulk(esConnection, generator(parquetToDict))
    

