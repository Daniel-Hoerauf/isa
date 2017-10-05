from django.shortcuts import HttpResponse
import requests

def hello(request):
    return HttpResponse('Hello main page\n')

def group(request):
     r = requests.get('https://api/group')
     return r
     #return HttpResponse('Hello main page\n')
