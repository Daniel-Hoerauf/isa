from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignupForm, LoginForm, NewGroupForm
from django.contrib import messages


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
        data = {}
        data['authenticator'] = request.COOKIES.get('authenticator')
        group = requests.post('http://exp-api:8000/group/{}/'.format(gid),
                             data).json()
        #reco = requests.post('http://exp-api:8000/recommendation/all').json()
        return render(request, 'group.html', group)


def signup(request):
    context = {}
    form = SignupForm
    if request.method == 'GET':
        #return render(request, 'signup.html', context)
        return render(request, 'signup.html', {'form':form})
    data = {}
    data['username'] = request.POST.get('username', '')
    data['password'] = request.POST.get('password', '')
    data['name'] = request.POST.get('name', '')
    data['year'] = request.POST.get('year', '')

    resp = requests.post('http://exp-api:8000/signup/', data)
    if resp.status_code != 200:
        return render(request, 'signup.html', {'form':form})
    resp = resp.json()
    if not resp or resp['status'] != 'ok':
        if resp['status'] == 'error':
            messages.add_message(request, messages.INFO, 'Username already exists')
        return render(request, 'signup.html', {'form':form})
    resp = requests.post('http://exp-api:8000/login/',data).json()
    if not resp or resp['status'] != 'ok':
        return render(request, 'login.html', {})
    authenticator = resp['authenticator']
    response = HttpResponseRedirect('/')
    response.set_cookie('authenticator', authenticator)
    return response

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
    form = LoginForm
    if request.method == 'GET':
        if request.COOKIES.get('authenticator') != None:
            return HttpResponseRedirect('/')
        return render(request, 'login.html', {'form':form})

    if request.method == 'POST':
        if request.COOKIES.get('authenticator') != None:
            return HttpResponseRedirect('/')
        data = {}
        data['username'] = request.POST.get('username', '')
        data['password'] = request.POST.get('password', '')
        if data['username'] == '' or data['password'] == '':
            return render(request, 'login.html', {'form':form})
        resp = requests.post('http://exp-api:8000/login/',data).json()
        if not resp or resp['authenticated'] != True:
            messages.add_message(request, messages.INFO, 'Login failed, please enter correct login info')
            return render(request, 'login.html', {'form':form})
        authenticator = resp['authenticator']
        response = HttpResponseRedirect('/')
        response.set_cookie('authenticator', authenticator)
    return response

def logout(request):
    data = {}
    data['authenticator'] = request.COOKIES.get('authenticator')
    resp = requests.post('http://exp-api:8000/logout/', data)
    response = HttpResponseRedirect('/')
    response.delete_cookie('authenticator')
    return response


def create_group(request):
    context = {}
    form = NewGroupForm
    if request.method == 'GET':
        data = {}
        authenticator = request.COOKIES.get('authenticator')
        if authenticator == None:
            return HttpResponseRedirect('/')
        data['authenticator'] = authenticator
        resp = requests.post('http://exp-api:8000/validate/', data).json()
        if resp['status'] == 'error':
            return HttpResponseRedirect('/')
        return render(request, 'newGroup.html', {'form':form})

    if request.method == 'POST':
        data = {}
        data['name'] = request.POST.get('name', '')
        data['size'] = request.POST.get('size', '')
        data['description'] = request.POST.get('description', '')
        data['loc'] = request.POST.get('loc', '')
        if data['name'] == '' or data['size'] == '' or data['description'] == '':
            return render(request, 'newGroup.html', {'form':form})
        resp = requests.post('http://exp-api:8000/creategroup/', data).json()

        if resp['status'] == 'ok':
            response = HttpResponseRedirect('/')
        else:
            response = HttpResponseRedirect('/newgroup')
        return response
