import csv
import json
import os
import pandas as pd

airflow_home = os.getenv('AIRFLOW_HOME')
data_path = airflow_home + '/data/raw_reading.csv'
transformed_path = airflow_home + '/data/transformed.parquet.gzip'

def transform_to_parquet(*args,**kwargs):
    raw_reading = pd.read_csv(data_path)
    dataframe = {'id':[],'data':[], 'timestamp':[] ,'local_time':[]}
    
    for i in range(len(raw_reading)):
        
        id = raw_reading.iloc[i]['id']
        value = json.loads(raw_reading.iloc[i]['value'])
        dataValue = value['data']
        timeValue = value['time']
        localTime = raw_reading.iloc[i]['local_time']
        
        dataframe['id'].append(id)
        dataframe['data'].append(dataValue)
        dataframe['timestamp'].append(timeValue)
        dataframe['local_time'].append(localTime)
        
    transformed = pd.DataFrame(dataframe).astype(str)
    transformed.to_parquet(transformed_path, index = False, compression='gzip')