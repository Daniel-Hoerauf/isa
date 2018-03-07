"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^admin/', admin.site.urls),
    url(r'^group/all/$', views.group_index, name='group_index'),
    url(r'^group/(?P<group>[0-9]+)/$', views.get_group, name='get_group'),
    # Authentication urls
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.create_user, name='signup'),
    url(r'^validate/$', views.validate, name='validate'),
    # Listings
    url(r'^creategroup/$', views.create_group, name='creategroup'),
    url(r'^search/$', views.search, name='search'),
    url(r'^recommendation/all/$', views.recommendation, name='rec_index')
]
