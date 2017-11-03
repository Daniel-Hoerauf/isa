from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render


import urllib.request
import urllib.parse
import json
import requests


def hello(request):
    
    #template_name = 'templates/mainPage/mainPage.html'
    
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
    if request.COOKIES.get('authenticator', 'none') == 'none':
        logged_in = 0
    else:
        logged_in = 1
    #return HttpResponse(logged_in)
    #return HttpResponse(request.COOKIES.get('authenticator', 'none'))
    #return HttpResponse(groupList)
    return render(request, 'mainPage.html', {'name':name, 'size':size, 'groupList':groupList, 'logged_in': logged_in})
    #return JsonResponse(resp)
    #return render(request, 'app/mainPage.html')
    

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
     #print(resp)
     #return HttpResponse('Hello group page\n')
     #return HttpResponse(size)
        return render(request, 'group.html', {'group':group})
        #return JsonResponse(resp)
def signup(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'signup.html', context)
    data = {}
    data['username'] = request.POST.get('username', '')
    data['password'] = request.POST.get('password', '')
    data['name'] = request.POST.get('name', '')
    data['year'] = request.POST.get('year', '')
    resp = requests.post('http://exp-api:8000/signup/', data)
    if resp.status_code != 200:
        return render(request, 'signup.html', context)
    resp = resp.json()
    if not resp or resp['status'] != 'ok':
        return render(request, 'signup.html', {})
    return HttpResponseRedirect('/')
    resp = requests.post('http://exp-api:8000/login/',data).json()
    if not resp or resp['status'] != 'ok':
        return render(request, 'login.html', {})
    authenticator = resp['authenticator']
    response = HttpResponseRedirect('/')
    response.set_cookie('authenticator', authenticator)

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
        resp = requests.post('http://exp-api:8000/login/',data).json()
        if not resp or resp['status'] != 'ok':
            return render(request, 'login.html', {})
        authenticator = resp['authenticator']
        response = HttpResponseRedirect('/')
        response.set_cookie('authenticator', authenticator)
        
    return response

def logout(request):
    data = {}
    data['authenticator'] = request.COOKIES.get('authenticator')
    resp = requests.post('http://exp-api:8000/logout/',data)
    response =  HttpResponseRedirect('/')
    response.delete_cookie('authenticator')
    return response
    
def create_group(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'newGroup.html', context)

    if request.method == 'POST':
        data = {}
        data['name'] = request.POST.get('name', '')
        data['size'] = request.POST.get('size', '')
        data['description'] = request.POST.get('description', '')
        data['loc'] = request.POST.get('loc', '')
        #if data['name'] == '' or data['size'] == None or data['description'] == '' or data['loc'] == '':
            #return render(request, 'newGroup.html', {})
        resp = requests.post('http://exp-api:8000/creategroup/',data)
        return HttpResponse(resp)
        
        if resp.status_code == 'ok':
            return hello(request)
        else:
            return render(request, 'newGroup.html', {})
