from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class registry(models.Model):
    signal = models.CharField(max_length=150)
    archival_active = models.BooleanField()
    first_registered = models.DateTimeField()
    last_altered = models.DateTimeField()

@python_2_unicode_compatible
class cpm(models.Model):
    measured_val = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{}: {}".format(self.timestamp, self.measured_val)
