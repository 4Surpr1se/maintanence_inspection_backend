# models.py
from django.db import models


class AircraftType(models.Model):
    """
    Model for aircraft type.
    """
    type = models.CharField(max_length=255, verbose_name="Aircraft Type")

    def __str__(self):
        return self.type


class Aircraft(models.Model):
    """
    Model for aircraft.
    """
    aircraft_type = models.ForeignKey('AircraftType', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[
        ('AVAILABLE', 'Available'),
        ('FLYING', 'Flying'),
        ('MAINTENANCE', 'Maintenance'),
    ], default='AVAILABLE', verbose_name="Aircraft Status")

    def __str__(self):
        return f"{self.aircraft_type.type} - {self.status}"


class Engineer(models.Model):
    """
    Model for engineer.
    """
    name = models.CharField(max_length=255, verbose_name="Engineer Name")
    aircraft_types = models.ManyToManyField('AircraftType', related_name='aircraft_types', blank=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    """
    Model for engineer's work with aircraft.
    """
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, verbose_name="Work Date")
    status = models.CharField(max_length=255, choices=[
        ('WORKING', 'Working'),
        ('VACATION', 'Vacation'),
        ('SICK_LEAVE', 'Sick Leave'),
    ], default='WORKING', verbose_name="Work Status")

    def __str__(self):
        return f"{self.engineer.name} - {self.aircraft.aircraft_type.type} - {self.date}"
