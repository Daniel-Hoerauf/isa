import json
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from time import sleep


def poll():
    es = Elasticsearch(['es'])
    consumer = KafkaConsumer('recommendations-topic', group_id='listing-indexer',
                             bootstrap_servers=['kafka:9092'])

    for message in consumer:
        with open('/data/access.log', 'a+') as log:
            access = json.loads((message.value).decode('utf-8'))
            log.write('{} {}\n'.format(access['user'], access['group']))


if __name__ == '__main__':
    sleep(120)
    poll()
