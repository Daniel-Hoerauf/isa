from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password

from .models import Location, Student, Group, User, Authenticator, Recommendation
from .models import create_authenticator, clean_authenticators

def index(request):
    return render(request, 'models.html')

def location_index(self):
    model = Location
    resp = {'status': 'ok', 'locations': []}
    for loc in Location.objects.all():
        resp['locations'].append({
            'id': loc.pk,
            'building_name': loc.building_name,
            'building_address': loc.building_address,
            'college_name': loc.college_name,
            })
    return JsonResponse(resp)

@require_POST
def add_location(request):
    building_name = request.POST.get("building_name")
    college_name = request.POST.get("college_name")
    building_address = request.POST.get("building_address")
    if None in [building_name, college_name, building_address]:
        return JsonResponse({'status': 'bad request'})
    location = Location(building_name=building_name, college_name=college_name,
                        building_address=building_address)
    location.save()
    loc_dict = {
        "building_name": location.building_name,
        "college_name": location.college_name,
        "building_address": location.building_address,
        }
    data = {}
    data['status'] = 'ok'
    data['result'] = loc_dict
    return JsonResponse(data)

def get_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    resp = {'status': 'ok', 'location': {
        'id': loc.pk,
        'building_name': loc.building_name,
        'college_name': loc.college_name,
        'building_address': loc.building_address,
    }}
    return JsonResponse(resp)


@require_POST
def delete_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    loc.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
def update_location(request, location):
    loc = get_object_or_404(Location, pk=location)
    name = request.POST.get('building_name')
    address = request.POST.get('building_address')
    college_name = request.POST.get('college_name')
    if name is None and address is None and college_name is None:
        return JsonResponse({'status': 'bad request'})
    updates = []
    if name:
        updates.append('building_name')
    if address:
        updates.append('building_address')
    if college_name:
        updates.append('college_name')
    loc.building_name = name
    loc.building_address = address
    loc.college_name = college_name
    loc.save(update_fields=updates)
    return JsonResponse({'status': 'ok'})


def student_index(request):
    resp = {'status': 'ok', 'students': []}
    for stud in Student.objects.all():
        resp['students'].append({
            'id': stud.pk,
            'name': stud.name,
            'year': stud.year,
            'groups': [{'id': gr.pk,
                        'name': gr.name}
                       for gr in stud.group_set.all()],
        })
    return JsonResponse(resp)


@require_POST
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
        'id': stud.pk,
        'name': stud.name,
        'year': stud.year,
        'groups': [{'id': gr.pk,
                    'name': gr.name}
                   for gr in stud.group_set.all()],
    }}
    return JsonResponse(resp)


@require_POST
def delete_student(request, student):
    stud = get_object_or_404(Student, pk=student)
    stud.delete()
    return JsonResponse({'status': 'ok'})

@require_POST
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
    resp = {'status': 'ok', 'groups': []}
    for grp in Group.objects.all():
        resp['groups'].append({
            'id':   grp.pk,
            'name': grp.name,
            'size': grp.size,
            'description': grp.description,
        })
    return JsonResponse(resp)

def recommendation(request):
    resp = {'status': 'ok', 'recs': []}
    for rec in Recommendation.objects.all():
        resp['recs'].append({
            'group_id': rec.group_id,
            'recommended_groups': rec.recommended_groups,
        })
    return JsonResponse(resp)


@require_POST
def create_group(request):
    name = request.POST.get('name')
    size = request.POST.get('size')
    description = request.POST.get('description')
    if None in [name, size]:
        return JsonResponse({'status': 'bad request'})
    group = Group.create(name, size, description)
    group.save()
    resp = {'status': 'ok', 'group': {
        'id': group.pk,
        'name': group.name,
        'size': group.size,
        'description': group.description,
    }}
    return JsonResponse(resp)


def get_group(request, group):
    group = get_object_or_404(Group, pk=group)
    try:
        rec = Recommendation.objects.get(group_id=group.pk)
    except Recommendation.DoesNotExist:
        rec = None
    if rec != None:
        resp = {'status': 'ok', 'recommendation': rec.recommended_groups, 'group': {
            'id': group.pk,
            'name': group.name,
            'size': group.size,
            'description': group.description,
        }}
    else:
        resp = {'status': 'ok', 'recommendation': 'None', 'group': {
            'id': group.pk,
            'name': group.name,
            'size': group.size,
            'description': group.description,
        }}
    return JsonResponse(resp)


@require_POST
def delete_group(request, group):
    group = get_object_or_404(Group, pk=group)
    group.delete()
    return JsonResponse({'status': 'ok'})


@require_POST
def update_group(request, group):
    group = get_object_or_404(Group, pk=group)
    name = request.POST.get('name')
    size = request.POST.get('size')
    description = request.POST.get('description')
    if name is None and size is None and description is None:
        return JsonResponse({'status': 'bad request'})
    updates = []
    if name:
        updates.append('name')
    if size:
        updates.append('size')
    if description:
        updates.append('description')
    group.name = name
    group.size = size
    group.description = description
    group.save(update_fields=updates)
    return JsonResponse({'status': 'ok'})


@require_POST
def remove_from_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    group = get_object_or_404(Group, pk=group)
    if stud in group.students.all():
        group.students.remove(stud)
    return JsonResponse({'status': 'ok'})

@require_POST
def add_to_group(request, group, student):
    stud = get_object_or_404(Student, pk=student)
    group = get_object_or_404(Group, pk=group)
    group.students.add(stud)
    return JsonResponse({'status': 'ok'})

@require_POST
def tag_group(request, group, location):
    loc = get_object_or_404(Location, pk=location)
    group = get_object_or_404(Group, pk=group)
    group.loc = loc
    group.save(update_fields=['loc'])
    return JsonResponse({'status': 'ok'})

@require_POST
def untag_group(request, group):
    group = get_object_or_404(Group, pk=group)
    group.loc = None
    group.save(update_fields=['loc'])
    return JsonResponse({'status': 'ok'})


@require_POST
def validate(request):
    auth = request.POST.get('authenticator', '')
    authenticator = get_object_or_404(Authenticator, pk=auth)
    # valid = str(user) == str(authenticator.user_id.pk)
    return JsonResponse({'status': 'ok',
                         'authenticated': True})


@require_POST
def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    name = request.POST.get('name')
    year = int(request.POST.get('year', "-1"))
    if None in [username, password, name] or year < 0:
        return JsonResponse({'status': 'bad request',
                             'authenticated': False,
                             'authenticator': None,
                             'message': 'Must have username, password, name, year'})
    student = Student.create(name, year)
    student.save()
    pass_hash = make_password(password)
    user = User(student=student, username=username, password=pass_hash)
    user.save()
    authenticator = create_authenticator(user)
    return JsonResponse({'status': 'ok',
                         'authenticated': True,
                         'authenticator': authenticator})


@require_POST
def login(request, user):
    password = request.POST.get('password', '')
    user = get_object_or_404(User, pk=user)
    if not check_password(password, user.password):
        return JsonResponse({'status': 'ok',
                             'authenticated': False,
                             'authenticator': None})
    authenticator = create_authenticator(user)
    return JsonResponse({'status': 'ok',
                         'authenticated': True,
                         'authenticator': authenticator})

@require_POST
def logout(request):
    auth = request.POST.get('authenticator')
    authenticator = get_object_or_404(Authenticator, pk=auth)
    authenticator.delete()
    clean_authenticators()
    return JsonResponse({'status': 'ok'})

@require_POST
def get_user_pk(request):
    username = request.POST.get('username')
    user = get_object_or_404(User, username=username)
    return JsonResponse({'status': 'ok',
                         'user': user.pk})

@require_POST
def get_user_from_authenticator(request):
    auth = request.POST.get('authenticator')
    authenticator = get_object_or_404(Authenticator, pk=auth)
    return JsonResponse({'status': 'ok',
                         'user': authenticator.user_id.pk})
