from django.conf.urls import include, url
from django.contrib import admin
from users import views

urlpatterns = [
    url(r'^$', views.userLogin, name='login'),
    url(r'^login/$', views.userLogin, name='login'),
    url(r'^logout/$', views.userLogout, name='logout'),
    url(r'^users$', views.usersView, name='usersView'),
    url(r'^user/register$', views.usersRegister, name='usersRegister'),
    url(r'^user/delete/(?P<sysuser_id>\d+)$', views.usersDelete, name='usersDelete'),
    url(r'^user/edit/(?P<sysuser_id>\d+)$', views.usersEdit, name='usersEdit'),
    url(r'^user/password$', views.usersPassword, name='usersPassword'),

]
