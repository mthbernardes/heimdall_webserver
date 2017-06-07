# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render,redirect
from clientes.models import Clientes
from vulnerabilities.models import Packages
from users.utils import group_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@group_required('admin','infra')
def update(request,vulnerability_id):
    package = Packages.objects.get(id=vulnerability_id)
    client = Clientes.objects.get(id=package.client.id)
    if package.status == 'vulnerable' or package.status == 'upgrade error':
        url = 'http://%s/api/v1/update' % client.ipaddr
        data = {'key':client.api,'packages':[package.package_name]}
        r = requests.post(url,json=data)
        package.status = 'waiting update'
        package.save(update_fields=["status"])
    return redirect('cliente',client.id)

@login_required(login_url='login')
def view(request,vulnerability_id):
    package = Packages.objects.get(id=vulnerability_id)
    return render(request,'view_vulnerability.html',{'package':package})
