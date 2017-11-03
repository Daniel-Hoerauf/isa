import json
import requests
from elasticsearch import Elasticsearch
from time import sleep
from kafka import KafkaConsumer

def initial_migration():
    es = Elasticsearch(['es'])
    resp = requests.post('http://models-api:8000/group/all/').json()
    for group in resp['groups']:
        es.index(index='listing_index', doc_type='listing', id=group['id'],
                 body=group)
    es.indices.refresh(index='listing_index')

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
    print('Sleeping for 15 seconds')
    sleep(15)
    print('Performing initial migration')
    initial_migration()
    print('Listening for new messages')
    poll()
