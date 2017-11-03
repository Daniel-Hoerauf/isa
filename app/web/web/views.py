from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import requests
import urllib.request
import urllib.parse
import json
import requests


def hello(request):

    req = urllib.request.Request('http://exp-api:8000/group/all')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    groupList = resp['groups']
    name = []
    size = []
    gid = []
    for i in groupList:
        name.append(i['name'])
        size.append(i['size'])
        gid.append(i['id'])

    return render(request, 'mainPage.html', {'name': name, 'size': size,
                                             'groupList': groupList})

def groupDetail(request):
    if request.method == 'GET':
        gid = request.GET.get('id')
        if gid is None:
            return HttpResponse("error")
        req = urllib.request.Request('http://exp-api:8000/group/all')
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        groups = resp['groups']
        group = groups
        for i in groups:
            if i['id'] == int(gid):
                group = i
                break
        return render(request, 'group.html', {'group': group})

def signup(request):
    pass

def search(request):
    query = request.GET.get('query')
    context = {}
    if query is None or query.strip() == '':
        context = {'searched': False}
    else:
        context = requests.get('http://exp-api:8000/search/',
                               {'query': query.strip()}).json()
        context['searched'] = True
    return render(request, 'search.html', context)

def login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'login.html', context)

    if request.method == 'POST':
        data = {}
        data['username'] = request.POST.get('username', '')
        data['password'] = request.POST.get('password', '')
        if data['username'] == '' or data['password'] == '':
            return render(request, 'login.html', {})
        resp = requests.post('http://exp-api:8000/login/',data)

        if resp.status_code == 'ok':
            return hello(request)
            #save authenticator
        else:
            return render(request, 'login.html', {})

def logout(request):
    data = {}
    #data['authenticator'] =
    resp = requests.post('http://exp-api:8000/logout/',data)

def create_group(request):
    data = {}
    data['name']='algo midterm'
    data['size']=4
    data['description']='last minute'

    context = {}
    if request.method == 'GET':
        return render(request, 'newGroup.html', context)
