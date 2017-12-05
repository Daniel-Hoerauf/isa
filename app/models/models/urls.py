from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Authentication endpoints
    url(r'^login/(?P<user>[0-9]+)/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.create_user, name='signup'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^get_user_pk/$', views.get_user_pk, name='get_user_pk'),
    url(r'^get_user_from_authenticator/$', views.get_user_from_authenticator,
        name='get_user_from_authenticator'),

    # Location endpoints
    url(r'^location/all/$', views.location_index, name='location_index'),
    url(r'^location/new/$', views.add_location, name='create_location'),
    url(r'^location/(?P<location>[0-9]+)/$', views.get_location,
        name='get_location'),
    url(r'^location/(?P<location>[0-9]+)/delete/$', views.delete_location,
        name='delete_location'),
    url(r'^location/(?P<location>[0-9]+)/update/$', views.update_location,
        name='update_location'),

    # Student Endpoints
    url(r'^student/all/$', views.student_index, name='student_index'),
    url(r'^student/new/$', views.create_student, name='create_student'),
    url(r'^student/(?P<student>[0-9]+)/$', views.get_student,
        name='get_student'),
    url(r'^student/(?P<student>[0-9]+)/delete/$', views.delete_student,
        name='delete_student'),
    url(r'^student/(?P<student>[0-9]+)/update/$', views.update_student,
        name='update_student'),

    # Group Endpoints
    url(r'^group/all/$', views.group_index, name='group_index'),
    url(r'^group/new/$', views.create_group, name='create_group'),
    url(r'^group/(?P<group>[0-9]+)/$', views.get_group,
        name='get_group'),
    url(r'^group/(?P<group>[0-9]+)/delete/$', views.delete_group,
        name='delete_group'),
    url(r'^group/(?P<group>[0-9]+)/update/$', views.update_group,
        name='update_group'),

    url(r'group/(?P<group>[0-9]+)/remove/(?P<student>[0-9]+)/',
        views.remove_from_group, name='remove_from_group'),
    url(r'group/(?P<group>[0-9]+)/add/(?P<student>[0-9]+)/',
        views.add_to_group, name='add_to_group'),

    url(r'group/(?P<group>[0-9]+)/tag/(?P<location>[0-9]+)/',
        views.tag_group, name='tag_group'),
    url(r'group/(?P<group>[0-9]+)/untag/',
        views.untag_group, name='untag_group'),
    url(r'^get_group_pk/$', views.get_group, name='get_group_pk'),
]
