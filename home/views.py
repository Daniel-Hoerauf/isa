from django.shortcuts import HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Location, Student, Group


def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")

def location_index(self):
    model = Location
    resp = {'status': 'ok', 'locations': []}
    for loc in Location.objects.all():
        resp['locations'].append({
            'building_name': loc.building_name,
            'building_address': loc.building_address,
            'college_name': loc.college_name,
            })
    return JsonResponse(resp)

def add_location(request):
    return HttpResponse("Add Location")

def get_location(request, location):
    return HttpResponse("Get Location #{}".format(location))

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

@require_POST
@csrf_exempt
def create_student(request):
    name = request.POST.get('name')
    year = request.POST.get('year')
    if None in [name, year]:
        return JsonResponse({'status': 'bad request'})
    stud = Student.create(name, year)
    stud.save()
    return JsonResponse({'status': 'ok'})


def get_student(request, student):
    stud = get_object_or_404(Student, pk=student)
    resp = {'status': 'ok', 'student': {
        'name': stud.name,
        'year': stud.year,
        'groups': [{'id': gr.pk,
                    'name': gr.name}
                   for gr in stud.group_set.all()],
    }}
    return JsonResponse(resp)


@require_POST
@csrf_exempt
def delete_student(request, student):
    stud = get_object_or_404(Student, pk=student)
    stud.delete()
    return JsonResponse({'status': 'ok'})

@require_POST
@csrf_exempt
def update_student(request, student):
    stud = get_object_or_404(Student, pk=student)
    name = request.POST.get('name')
    year = request.POST.get('year')
    if name is None and year is None:
        return JsonResponse({'status': 'bad request'})
    updates = []
    if name:
        updates.append('name')
    if year:
        updates.append('year')
    stud.name = name
    stud.year = year
    stud.save(update_fields=updates)
    return JsonResponse({'status': 'ok'})



def group_index(request):
    resp = {'status': 'empty', 'groups': []}
    for grp in Group.objects.all():
        resp['groups'].append({
            'name': grp.name,
            'size': grp.size,
        })
    return JsonResponse(resp)

def create_group(request):
    return HttpResponse("Create Group")

def get_group(request, group):
    return HttpResponse("Get Group #{}".format(group))

def delete_group(request, group):
    return HttpResponse("Delete Group #{}".format(group))

def update_group(request, group):
    return HttpResponse("Update Group #{}".format(group))


@require_POST
@csrf_exempt
def remove_from_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    group = get_object_or_404(Group, pk=group)
    if stud in group.student:
        group.students.remove(stud)
    return JsonResponse({'status': 'ok'})

@require_POST
@csrf_exempt
def add_to_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    group = get_object_or_404(Group, pk=group)
    group.students.add(stud)
    return JsonResponse({'status': 'ok'})

@require_POST
@csrf_exempt
def tag_group(request, group, location):
    loc = get_object_or_404(Location, pk=location)
    group = get_object_or_404(Group, pk=group)
    group.loc = loc
    group.save(update_fields=['loc'])
    return JsonResponse({'status': 'ok'})

@require_POST
@csrf_exempt
def untag_group(request, group):
    group = get_object_or_404(Group, pk=group)
    group.loc = None
    group.save(update_fields=['loc'])
    return JsonResponse({'status': 'ok'})
