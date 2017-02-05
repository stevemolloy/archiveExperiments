from __future__ import unicode_literals

from django.db import models

class registry(models.Model):
    signal = models.CharField(max_length=150)
    archival_active = models.BooleanField()
    first_registered = models.DateTimeField()
    last_altered = models.DateTimeField()

class cpm(models.Model):
    measured_val = models.IntegerField()
    timestamp = models.DateTimeField()
