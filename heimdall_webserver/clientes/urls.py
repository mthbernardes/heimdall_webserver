from django.conf.urls import include, url
from django.contrib import admin
from clientes import views

urlpatterns = [
    url(r'^clientes$', views.clientes, name='clientes'),
    url(r'^cliente/(?P<cliente_id>\d+)$', views.cliente, name='cliente'),
    url(r'^cliente/remove/(?P<cliente_id>\d+)$', views.delete, name='delete'),
    url(r'^cliente/cadastrar$', views.cadastrar, name='cadastrar'),
    url(r'^cliente/editar/(?P<cliente_id>\d+)$', views.editar, name='editar'),
]
