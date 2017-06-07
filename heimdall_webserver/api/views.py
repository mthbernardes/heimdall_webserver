# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse
from clientes.models import Clientes
from django.views.decorators.csrf import csrf_exempt
from vulnerabilities.models import Packages

@csrf_exempt
def beat(requests):
    if requests.method == 'POST':
        client = getCliente(requests.POST)
        if client:
            client.lastupdate = timezone.now()
            client.save(update_fields=["lastupdate"])
            return HttpResponse(json.dumps({'status':'ok'}))
    return HttpResponse(json.dumps({'response':'not ok'}),content_type="application/json")

@csrf_exempt
def vulnerabilities(requests):
    if requests.method == 'POST':
        data = requests.POST
        client = getCliente(data)
        if client:
            beat(requests)
            packages = data.getlist('packages')
            for package in packages:
                p, created = Packages.objects.get_or_create(package_name=package,client=client)
                print created
            return HttpResponse(json.dumps({'status':'ok'}))
    return HttpResponse(json.dumps({'response':'not ok'}),content_type="application/json")

@csrf_exempt
def status(requests):
    if requests.method == 'POST':
        data = requests.POST
        client = getCliente(data)
        package = Packages.objects.get(package_name=data['package_name'],client=client.id)
        package.status = data['vulnerability_status']
        package.update_response = data['upgrade_status']
        package.save(update_fields=["status","update_response"])
        return HttpResponse(json.dumps({'status':'ok'}))
    return HttpResponse(json.dumps({'response':'not ok'}),content_type="application/json")

def getCliente(data):
    try:
        client = Clientes.objects.get(api=data['key'])
    except:
        client = None
    return client
