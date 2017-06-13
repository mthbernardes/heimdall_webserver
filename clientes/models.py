# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Clientes(models.Model):
    name = models.CharField(max_length=255, null=False)
    ipaddr = models.CharField(max_length=15, null=False)
    distro = models.CharField(max_length=255, null=False)
    api = models.CharField(max_length=36,null=False)
    lastupdate = models.DateTimeField(auto_now_add=False,null=True)

    @property
    def update_status(self,):
        time = timezone.now() - Clientes.objects.get(id=self.id).lastupdate
        if time.seconds < 20:
            return True
        else:
            return False
