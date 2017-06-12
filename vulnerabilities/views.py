# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render,redirect
from clientes.models import Clientes
from django.contrib.auth.models import User
from vulnerabilities.models import Comments
from vulnerabilities.models import Packages
from users.utils import group_required
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
@group_required('admin','infra')
def update(request,vulnerability_id):
    package = Packages.objects.get(id=vulnerability_id)
    client = Clientes.objects.get(id=package.client.id)
    url = 'http://%s/api/v1/update' % client.ipaddr
    try:
        r = requests.get(url,timeout=2)
    except:
        r = None
    if r:
        if package.status == 'vulnerable' or package.status == 'upgrade error':
            print 'Entrou'
            data = {'key':client.api,'packages':[package.package_name]}
            r = requests.post(url,json=data)
            package.status = 'waiting update'
            package.save(update_fields=["status"])
    return redirect('cliente',client.id)

@login_required(login_url='login')
def view(request,vulnerability_id):
    package = Packages.objects.get(id=vulnerability_id)
    comments = Comments.objects.filter(package_id=vulnerability_id)
    return render(request,'view_vulnerability.html',{'package':package,'comments':comments})

@login_required(login_url='login')
def addComment(request,package_id):
    package = Packages.objects.get(id=package_id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        data = request.POST
        Comments(package_id=package,user=user,comment=data['comment']).save()
    return redirect('view',package_id)
