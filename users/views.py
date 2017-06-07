# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,render_to_response,HttpResponseRedirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.utils import group_required

def userLogin(requests):
    if requests.user.is_authenticated():
        return redirect('clientes')
    if requests.method == 'POST':
        data = requests.POST
        user = authenticate(requests, username=data['username'], password=data['password'])
        if user is not None:
            login(requests,user)
            return redirect('clientes')
        else:
            return render(requests,'login.html',{"error":"check your credentials"})
    return render(requests,'login.html')

@login_required(login_url='login')
def userLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def usersPassword(requests):
    sysuser = User.objects.get(id=requests.user.id)
    if requests.method == 'POST':
        data = requests.POST
        if sysuser.check_password(data['actual_password']) and data['new_password'] == data['conf_password']:
            sysuser.set_password(data['new_password'])
            sysuser.save()
        return redirect('clientes')
    return render(requests,'user_password.html')

@login_required(login_url='login')
@group_required('admin')
def usersView(requests):
    users = User.objects.all()
    return render(requests,'users.html',{'sysusers':users})


@login_required(login_url='login')
@group_required('admin')
def usersRegister(requests):
    groups = Group.objects.all()
    if requests.method == 'POST':
        data = requests.POST
        user = User.objects.create_user(username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'])
        user.groups.add(Group.objects.get(name=data['group']))
        return redirect('usersView')
    return render(requests,'user_register.html',{'groups':groups})

@login_required(login_url='login')
@group_required('admin')
def usersEdit(requests,sysuser_id):
    groups = Group.objects.all()
    sysuser = User.objects.get(id=sysuser_id)
    if requests.method == 'POST':
        data = requests.POST
        sysuser.email= data['email']
        sysuser.first_name= data['first_name']
        sysuser.last_name= data['last_name']
        sysuser.save(update_fields=["email","first_name","last_name"])
        user_group = User.groups.through.objects.get(user=User.objects.get(id=sysuser_id))
        user_group.group = Group.objects.get(name=data['group'])
        user_group.save()
        return redirect('usersView')
    return render(requests,'user_register.html',{'sysuser':sysuser,'groups':groups})

@login_required(login_url='login')
@group_required('admin')
def usersDelete(requests,sysuser_id):
    if requests.user.id != int(sysuser_id):
        users = User.objects.get(id=sysuser_id).delete()
    return redirect('usersView')
