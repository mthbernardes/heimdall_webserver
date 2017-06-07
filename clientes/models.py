# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Clientes(models.Model):
    name = models.CharField(max_length=255, null=False)
    ipaddr = models.CharField(max_length=15, null=False)
    distro = models.CharField(max_length=255, null=False)
    api = models.CharField(max_length=36,null=False)
    lastupdate = models.DateTimeField(auto_now_add=False,null=True)
