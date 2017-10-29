from django.shortcuts import render, HttpResponse
import urllib.request
import urllib.parse
from django.core.urlresolvers import reverse
import json
import requests
from django.http import JsonResponse


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
    #data dict is only to be used until web layer is complete
    data = {}
    data['username'] = 'tester'
    data['name'] = 'brigham'
    data['password'] = 'notpassword'
    data['year'] = 4
    resp = requests.post('http://models-api:8000/get_user_pk/',data)
    if resp.status_code != 404:
        return JsonResponse({'status':'error'})
    resp = requests.post('http://models-api:8000/signup/',data).json()
    return JsonResponse(resp)

def login(request):
    data = {}
    data['username'] = 'tester'
    data['name'] = 'brigham'
    data['password'] = 'notpassword'
    data['year'] = 4
    resp = requests.post('http://models-api:8000/get_user_pk/',data)
    return HttpResponse(resp)
    string = 'http://models-api:8000/login/'
    string += resp['user']
    resp = requests.post(string).json()
    return JsonResponse(resp)
    #return JsonResponse(resp)
    #return JsonResponse({'status': 'ok'})

def logout(request):
    string = 'http://models-api:8001/login/'
    string+= user.pk
    resp = requests.post(string).json()
    return JsonResponse(resp)

def create_group(request):
    string = 'http://models-api:8001/group/new/'
    data = {}
    data['name']='algo midterm'
    data['size']=4
    data['description']='last minute'
    resp = requests.post(string,data).json()
    return JsonResponse(resp)
    
