# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from clientes.models import Clientes

class Packages(models.Model):
    package_name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=20,default='vulnerable')
    update_response = models.TextField(default='',null=False)
    client = models.ForeignKey(Clientes,related_name='client')
