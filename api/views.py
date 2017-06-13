# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse
from clientes.models import Clientes
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from vulnerabilities.models import Packages,Exploit,CVE

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
        data = json.loads(requests.body)
        client = getCliente(data)
        if client:
            beat(requests)
            for package in data['packages']:
                p, created = Packages.objects.get_or_create(package_name=package,client=client)
                for cve in data['packages'][package]:
                    c, created = CVE.objects.get_or_create(cveid=cve,package_id=p)
                    if len(data['packages'][package][cve][0]) > 0:
                        desc,xpl = data['packages'][package][cve]
                        for i in range(0,len(desc)):
                            e, created = Exploit.objects.get_or_create(description=desc[i],exploit_url=xpl[i],cve_id=c)
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
    except Exception as e:
        print e
        client = None
    return client
