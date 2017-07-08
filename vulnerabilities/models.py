# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from clientes.models import Clientes
from django.contrib.auth.models import User

class Packages(models.Model):
    package_name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=20,default='vulnerable')
    update_response = models.TextField(default='',null=False)
    client = models.ForeignKey(Clientes,related_name='client')

class CVE(models.Model):
    cveid = models.CharField(max_length=20, null=False)
    package_id = models.ForeignKey(Packages,related_name='package')
    
    @property
    def exploits(self,):
        return Exploit.objects.filter(cve_id=self)

class Exploit(models.Model):
    description = models.TextField(null=True)
    exploit_url = models.CharField(max_length=255, null=True)
    cve_id = models.ForeignKey(CVE,related_name='cve_id')

class Comments(models.Model):
    comment = models.TextField(default='',null=False)
    package_id = models.ForeignKey(Packages,related_name='package_id')
    user = models.ForeignKey(User,related_name='user')
