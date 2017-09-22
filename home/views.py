from django.shortcuts import HttpResponse, get_object_or_404
from django.http import JsonResponse
from .models import Location, Student
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

@csrf_exempt
def add_location(request):
    if request.method == "POST":
        location = Location()
        location.building_name = request.POST.get("building name", "")
        location.college_name = request.POST.get("college name", "")
        location.building_address = request.POST.get("building address", "")
        location.save()
        loc_dict = {
            "building name": location.building_name,
            "college name": location.college_name,
            "building address": location.building_address,
            }
        data = {}
        data['ok'] = True
        data['message'] = "Success"
        data['result'] = loc_dict
        return JsonResponse(data)
    else:
        data = {}
        data['ok'] = False
        data['message'] = "ERROR: Item must be a post request"
        return JsonResponse(data)

@csrf_exempt
def get_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    resp = {'status': 'empty', 'location': {
        'building name': location.building_name,
        'building address': location.building_address,
    }}
    return JsonResponse(resp)


@require_POST
@csrf_exempt
def delete_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    loc.delete()
    return JsonResponse({'status': 'okd'})


@require_POST
@csrf_exempt
def update_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    name = request.POST.get('building name')
    address = request.POST.get('building address')
    if name is None and address is None:
        return JsonResponse({'status': 'bad request'})
    updates = []
    if name:
        updates.append('building name')
    if address:
        updates.append('building address')
    loc.building_name = name
    loc.building_address = address
    loc.save(update_fields=updates)
    return JsonResponse({'status': 'ok'})


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


@require_POST
@csrf_exempt
def create_group(request):
    name = request.POST.get('name')
    size = request.POST.get('size')
    if None in [name, size]:
        return JsonResponse({'status': 'bad request'})
    group = Group.create(name, size)
    group.save()
    return JsonResponse({'status': 'ok'})


def get_group(request, group):
    group = get_object_or_404(Group, pk=group)
    resp = {'status': 'ok', 'group': {
        'name': group.name,
        'size': group.size,
    }}
    return JsonResponse(resp)


@require_POST
@csrf_exempt
def delete_group(request, group):
    group = get_object_or_404(Group, pk=group)
    group.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
@csrf_exempt
def update_group(request, group):
    group = get_object_or_404(Group, pk=group)
    name = request.POST.get('name')
    size = request.POST.get('size')
    if name is None and size is None:
        return JsonResponse({'status': 'bad request'})
    updates = []
    if name:
        updates.append('name')
    if size:
        updates.append('size')
    group.name = name
    group.size = size
    group.save(update_fields=updates)
    return HttpResponse("Update Group #{}".format(group))


@require_POST
@csrf_exempt
def remove_from_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    if stud is None:
        return JsonResponse({'status': 'ERROR: Student not found'})
    group = get_object_or_404(Group, pk=group)
    if group is None:
        return JsonResponse({'status':'ERROR: Group not found'})
    if stud in group.student:
        group.students.remove(stud)
    return JsonResponse({'status': 'ok'})

@require_POST
@csrf_exempt
def add_to_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    if stud is None:
        return JsonResponse({'status': 'ERROR: Student not found'})
    group = get_object_or_404(Group, pk=group)
    if group is None:
        return JsonResponse({'status':'ERROR: Group not found'})
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
