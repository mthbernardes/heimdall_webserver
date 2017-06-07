# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from uuid import uuid4
from django.utils import timezone
from humanize import naturaltime
from users.utils import group_required
from django.shortcuts import render,redirect
from clientes.models import Clientes
from vulnerabilities.models import Packages
from django.contrib.auth.decorators import login_required,user_passes_test

@login_required(login_url='login')
def clientes(request):
    clientes = Clientes.objects.all()
    return render(request,'clientes.html',{'clientes':clientes})

@login_required(login_url='login')
def cliente(request,cliente_id):
    cliente = Clientes.objects.get(id=cliente_id)
    packages = getVulnerabilities(cliente_id)
    if cliente.lastupdate:
        last_update = getupdate(cliente)
    else:
        last_update = 'never connected :/'
    return render(request,'cliente.html',{'cliente':cliente,'last_update':last_update,'packages':packages})


@login_required(login_url='login')
@group_required('admin','infra')
def delete(request,cliente_id):
    Clientes.objects.get(id=cliente_id).delete()
    return redirect('clientes')

@login_required(login_url='login')
@group_required('admin','infra')
def cadastrar(request):
    if request.method == 'POST':
        data = request.POST
        token = str(uuid4())
        Clientes(name=data['name'],ipaddr=data['ipaddr'],distro=data['distro'],api=token).save()
        return redirect('clientes')
    return render(request, 'cadastrar.html')

@login_required(login_url='login')
@group_required('admin','infra')
def editar(request,cliente_id):
    client = Clientes.objects.get(id=cliente_id)
    if request.method == 'POST':
        data = request.POST
        client.name = data['name']
        client.ipaddr = data['ipaddr']
        client.distro = data['distro']
        client.save(update_fields=["name","ipaddr","distro"])
        return redirect('clientes')
    return render(request,'cadastrar.html',{'cliente':client})

def getVulnerabilities(cliente_id):
    packages = Packages.objects.filter(client_id=cliente_id).all
    return packages

def getupdate(cliente):
    last_update = naturaltime(timezone.now() - cliente.lastupdate)
    return last_update
