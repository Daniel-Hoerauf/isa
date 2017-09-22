from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import Location, Student


def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")

def location_index(self):
    model = Location
    resp = {'status': 'empty', 'locations': []}
    for loc in Location.objects.all():
        resp['locations'].append({
            'building_name':loc.building_name,
            'building_address': loc.building_address,
            'college_name': loc.college_name,
            })
    return JsonResponse(resp)

def add_location(request):
    return HttpResponse("Add Location")

def get_location(request, location):
    return HttpResponse("Get Location #{{".format(location))
                                         
def delete_location(request, location):
    return HttpResponse("Delete Location #{}".format(location))

def update_location(request, location):
    return HttpResponse("Delete Location #{}".format(location))

def student_index(request):
    resp = {'status': 'ok', 'students': []}
    for stud in Student.objects.all():
        resp['students'].append({
            'name': stud.name,
            'year': stud.year,
            'groups': [{'id': gr.pk,
                        'name': gr.name}
                       for gr in stud.group_set.all()],
        })
    return JsonResponse(resp)

def create_student(request):
    return HttpResponse("Create Student")

def get_student(request, student):
    return HttpResponse("Get Student #{}".format(student))

def delete_student(request, student):
    return HttpResponse("Delete Student #{}".format(student))

def update_student(request, student):
    return HttpResponse("Update Student #{}".format(student))