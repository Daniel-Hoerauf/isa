from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import requests
import urllib.request
import urllib.parse
import json


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
    return JsonResponse(resp)


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
    # req = requests.post('http://exp-api:8000/signup', )

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
