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

class Comments(models.Model):
    comment = models.TextField(default='',null=False)
    package_id = models.ForeignKey(Packages,related_name='package_id')
    user = models.ForeignKey(User,related_name='user')
