from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests
from django.http import JsonResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch


def hello(request):
    return render(request, 'exp.html')

def group(request):
    req = urllib.request.Request('http://models-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def group_index(request):
    req = urllib.request.Request('http://models-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def get_group(request, group):
    req = urllib.request.Request('http://models-api:8000/group/1')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

def create_user(request):
    # data dict is only to be used until web layer is complete
    data = {}
    data['username'] = 'tester'
    data['name'] = 'brigham'
    data['password'] = 'notpassword'
    data['year'] = 4
    resp = requests.post('http://models-api:8000/get_user_pk/', data)
    if resp.status_code != 404:
        return JsonResponse({'status': 'error'})
    resp = requests.post('http://models-api:8000/signup/', data).json()
    return JsonResponse(resp)

def login(request):
    data = {}
    data['username'] = 'tester'
    data['name'] = 'brigham'
    data['password'] = 'notpassword'
    data['year'] = 4
    resp = requests.post('http://models-api:8000/get_user_pk/', data)
    if resp.status_code == 404:
        return JsonResponse({'status': 'error'})
    resp = resp.json()
    string = 'http://models-api:8000/login/'
    string += str(resp['user']) + "/"
    resp = requests.post(string, data).json()
    return JsonResponse(resp)

def logout(request):
    data = {}
    data['authenticator'] = 'b76104d4774bafe5d0cb50f5f6132863da9627770b9b60b13c99e375cb698c61'
    resp = requests.post('http://models-api:8000/logout/', data).json()
    return JsonResponse(resp)

def create_group(request):
    data = {}
    data['name'] = 'algo midterm'
    data['size'] = 4
    data['description'] = 'last minute'

    # Add to kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    some_new_group = {'name': data['name'], 'size': data['size'], 'description': data['description']}
    producer.send('new-listing-topic', json.dumps(some_new_group).encode('utf-8'))

    resp = requests.post('http://models-api:8000/group/new/', data).json()
    return JsonResponse(resp)


def search(request):
    query = request.GET.get('query')
    es = Elasticsearch(['es'])
    search = es.search(index='listing_index',
                       body={'query': {'query_string': {'query': query}},
                             'size': 10})
    hits = [hit['_source'] for hit in search['hits']['hits']]
    return JsonResponse({'valid': (search['hits']['total'] != 0),
                         'hits': hits})
