#!/usr/bin/env bash

if test ! -f "/.initindex" ; then
    #copy mapping from satu's index into local index.
    elasticdump --input=https://${SATU_USERNAME}:${SATU_PASSWORD}@satu-production.es.ap-southeast-1.aws.found.io:9243/sda_alerts --output=http://elastic:${ELASTIC_PASSWORD}@es:9200/sda_test --type=mapping

    #copy data from satu into local elasticsearch
    elasticdump --input=https://${SATU_USERNAME}:${SATU_PASSWORD}@satu-production.es.ap-southeast-1.aws.found.io:9243/sda_alerts --output=http://elastic:${ELASTIC_PASSWORD}@es:9200/sda_test --searchBody="{\"query\": {\"bool\":{\"must\": {\"match\": {\"alert_at_date\": \"2022-04-02\"}}}}}" --type=data

    touch /.initindex
else
    echo "Init skipped, index has been initialized before."
fi

