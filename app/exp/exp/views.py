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
    resp = requests.post('http://models-api:8000/signup/',data).json()
    return JsonResponse(resp)

def login(request):
    resp = requests.post(reverse('login', args=[user.pk]),{'password': 'p4ssw0rd'}).json()
    if resp['status']=='ok' and resp['authenticated']==True:
        auth = Authenticator.objects.get(pk=resp['authenticator'])
        if auth.user_id == user:
            return True
    return False
    #return JsonResponse(resp)
    #return JsonResponse({'status': 'ok'})

def logout(request):
    auth = create_authenticator(user)
    if Authenticator.objects.get(authenticator=auth) == True:
        resp = requests.post(reverse('logout'), {'authenticator': auth}).json()
    return JsonResponse(resp)
