from django.conf.urls import include, url
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^api/v1/heartbeat$', views.beat, name='beat'),
    url(r'^api/v1/vulnerabilities$', views.vulnerabilities, name='vulnerabilities'),
    url(r'^api/v1/vulnerability/status$', views.status, name='status'),
]
