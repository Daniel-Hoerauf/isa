from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    
    #location get requests
    url(r'^location/all/$', views.location_index, name='location_index'),
    url(r'^location/new/$', views.add_location, name='add_location'),
    url(r'^location/(?P<location>[0-9]+)/$', views.get_location,
        name='get_location'),
    url(r'^location/(?P<location>[0-9]+)/delete/$', views.delete_location,
        name='delete_location'),
    url(r'^location/(?P<location>[0-9]+)/update/$', views.update_location,
        name='update_location'),
    
    #Student get requests
    url(r'^student/all/$', views.student_index, name='student_index'),
    url(r'^student/new/$', views.create_student, name='create_student'),
    url(r'^student/(?P<student>[0-9]+)/$', views.get_student,
        name='get_student'),
    url(r'^student/(?P<student>[0-9]+)/delete/$', views.delete_student,
        name='delete_student'),
    url(r'^student/(?P<student>[0-9]+)/update/$', views.update_student,
        name='update_student'),
]