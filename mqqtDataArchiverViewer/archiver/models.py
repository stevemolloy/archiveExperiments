from __future__ import unicode_literals

from django.db import models

class cpm(models.Model):
    measured_val = models.IntegerField()
    timestamp = models.DateTimeField()
