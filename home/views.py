from django.shortcuts import render, HttpResponse
from django.db import models
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from .models import Location


def index(request):
    return HttpResponse("<h1>Hello, world.</h1>")

class LocationView(generic.DetailView):
    def get_queryset(self):
        model = Location
        template_name = 'home/location.html'
        loc_index_dict = {}
        for loc in Location.objects.all():
            print(loc.building_name)
            loc_index_dict["building name"] = loc.building_name
            loc_index_dict["college name"] = loc.college_name
            loc_index_dict["building address"] = loc.building_address
        return JsonResponse(loc_index_dict)

