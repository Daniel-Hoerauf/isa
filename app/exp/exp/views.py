from django.shortcuts import render
from redis import StrictRedis
import urllib.request
import urllib.parse
import json
import requests
from django.http import JsonResponse, HttpResponse
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt

def hello(request):
    return render(request, 'exp.html')

def group_index(request):
    r = StrictRedis(host='redis', port=6379, db=0)
    if r.get('all') is not None:
        return JsonResponse(json.loads(r.get('all').decode('utf-8')))
    req = urllib.request.Request('http://models-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    r.set('all', resp_json)
    resp = json.loads(resp_json)
    return JsonResponse(resp)


def recommendation(request):
    req = urllib.request.Request('http://models-api:8000/recommendation/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp)

@csrf_exempt
def get_group(request, group):
    # Add to kafka
    user = requests.post('http://models-api:8000/get_user_from_authenticator/',
                         {'authenticator': request.POST.get('authenticator')}).json()['user']
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    producer.send('recommendations-topic', json.dumps({'user': user,
                                                       'group': group}
                                                      ).encode('utf-8'))

    r = StrictRedis(host='redis', port=6379, db=0)
    if r.get(group) is not None:
        return JsonResponse(json.loads(r.get(group).decode('utf-8')))
    reco = urllib.request.Request('http://models-api:8000/recommendation/all')
    reco_json = urllib.request.urlopen(req).read().decode('utf-8')
    req = urllib.request.Request('http://models-api:8000/group/{}'.format(group))
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    r.set(group, resp_json)
    return JsonResponse(resp)

@csrf_exempt
def create_user(request):
    data = {}
    data['username'] = request.POST.get('username', '')
    data['password'] = request.POST.get('password', '')
    data['name'] = request.POST.get('name', '')
    data['year'] = request.POST.get('year', '')
    resp = requests.post('http://models-api:8000/get_user_pk/', data)
    if resp.status_code != 404:
        return JsonResponse({'status': 'error', 'message': 'username already taken'})
    resp = requests.post('http://models-api:8000/signup/', data).json()
    return JsonResponse(resp)

@csrf_exempt


def login(request):
    data = {}
    data['username'] = request.POST.get('username', '')
    data['password'] = request.POST.get('password', '')
    resp = requests.post('http://models-api:8000/get_user_pk/', data)
    if resp.status_code == 404:
        return JsonResponse({'status': 'error'})
    resp = resp.json()
    string = 'http://models-api:8000/login/'
    string += str(resp['user']) + "/"
    resp = requests.post(string, data).json()
    return JsonResponse(resp)

@csrf_exempt
def logout(request):
    data = {}
    data['authenticator'] = request.POST.get('authenticator', '')
    resp = requests.post('http://models-api:8000/logout/', data).json()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def create_group(request):
    data = {}
    data['name'] = request.POST.get('name', '')
    data['size'] = request.POST.get('size', '')
    data['description'] = request.POST.get('description', '')
    data['loc'] = request.POST.get('loc', '')

    resp = requests.post('http://models-api:8000/group/new/', data).json()
    if resp['status'] != 'ok':
        return JsonResponse(resp)

    r = StrictRedis(host='redis', port=6379, db=0)
    # Clear the cache for all whenever new group is added
    r.delete('all')
    # Add to kafka
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    producer.send('new-listings-topic', json.dumps(resp['group']).encode('utf-8'))

    return JsonResponse(resp)

@csrf_exempt
def search(request):
    query = request.GET.get('query')
    es = Elasticsearch(['es'])
    search = es.search(index='listing_index',
                       body={'query': {'query_string': {'query': query}},
                             'size': 10})
    hits = [hit['_source'] for hit in search['hits']['hits']]
    return JsonResponse({'valid': (search['hits']['total'] != 0),
                         'hits': hits})
@csrf_exempt
def validate(request):
    data = {}
    data['authenticator'] = request.POST.get('authenticator')
    resp = requests.post('http://models-api:8000/validate/', data)
    if resp.status_code == 404:
        return JsonResponse({'status': 'error'})
    return JsonResponse(resp.json())
