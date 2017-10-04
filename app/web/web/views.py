from django.shortcuts import HttpResponse

def hello(request):
    return HttpResponse('Hello main page\n')

def group(request):
     return render_to_response('http://8001/group/all',.....)
