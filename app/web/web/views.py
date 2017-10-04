from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hello World\n')

def group(request):
    return HttpResponse('Group Page\n')
