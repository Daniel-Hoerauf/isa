import json
from elasticsearch import Elasticsearch
from time import sleep
from kafka import KafkaConsumer


def poll():
    es = Elasticsearch(['es'])
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer',
                             bootstrap_servers=['kafka:9092'])

    for message in consumer:
        listing = json.loads((message.value).decode('utf-8'))
        es.index(index='listing_index', doc_type='listing', id=listing['id'],
                 body=listing)
        es.indices.refresh(index='listing_index')


if __name__ == '__main__':
    sleep(15)
    poll()
