from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hello World\n')

def group(request):
    return HttpResponse('api group\n')
