from django.conf.urls import include, url
from django.contrib import admin
from vulnerabilities import views

urlpatterns = [
    url(r'^vulnerability/update/(?P<vulnerability_id>\d+)$', views.update, name='update'),
    url(r'^vulnerability/view/(?P<vulnerability_id>\d+)$', views.view, name='view'),
    url(r'^vulnerability/comment/add/(?P<package_id>\d+)$', views.addComment, name='addComment'),
]
