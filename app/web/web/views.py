from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hello main page\n')

def group(request):
    return HttpResponse('Group Page\n')
