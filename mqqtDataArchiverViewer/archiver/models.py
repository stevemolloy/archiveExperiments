from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class registry(models.Model):
    signal = models.CharField(max_length=150)
    archival_active = models.BooleanField()
    first_registered = models.DateTimeField()
    last_altered = models.DateTimeField()

    def __str__(self):
        return "{}: {}".format(self.signal, self.archival_active)

@python_2_unicode_compatible
class cpm(models.Model):
    measured_val = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{}: {}".format(self.timestamp, self.measured_val)

class KlystronBodyWaterSystem(models.Model):
    body_flow = models.FloatField()
    body_temp = models.FloatField(null=True)
    timestamp = models.DateTimeField()

class ModOilTankWaterSystem(models.Model):
    tank_flow = models.FloatField()
    tank_temp = models.FloatField(null=True)
    timestamp = models.DateTimeField()

class KlystronCollectorWaterSystem(models.Model):
    collector_flow = models.FloatField()
    collector_temp = models.FloatField(null=True)
    timestamp = models.DateTimeField()

class KlystronSolenoidWaterSystem(models.Model):
    solenoid_flow = models.FloatField()
    solenoid_temp = models.FloatField(null=True)
    timestamp = models.DateTimeField()

class InputWaterSystem(models.Model):
    input_flow = models.FloatField(null=True)
    input_temp = models.FloatField()
    timestamp = models.DateTimeField()

class TestStandEnvironment(models.Model):
    light = models.FloatField()
    light_averaged = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField()

class RFPowerMeter(models.Model):
    input1 = models.FloatField()
    input2 = models.FloatField()
    timestamp = models.DateTimeField()
