from django.db import models
from django.db.models.query import QuerySet
from django_group_by import GroupByMixin


class WorkQuerySet(QuerySet, GroupByMixin):
    pass


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
    aircraft_sn = models.CharField(max_length=255, verbose_name="Aircraft SN", unique=True)
    aircraft_type = models.ForeignKey('AircraftType', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=[
        ('AVAILABLE', 'Available'),
        ('FLYING', 'Flying'),
        ('MAINTENANCE', 'Maintenance'),
    ], default='AVAILABLE', verbose_name="Aircraft Status")

    def __str__(self):
        return f"{self.aircraft_type.type} - {self.status}"

    @staticmethod
    def get_spawn():
        return \
            Aircraft.objects.get_or_create(
                aircraft_sn='NAN',
                aircraft_type=AircraftType.objects.get_or_create(type='NAN')[0])[0]


class Engineer(models.Model):
    """
    Model for engineer.
    """
    name = models.CharField(max_length=255, verbose_name="Engineer Name")
    surname = models.CharField(max_length=255, verbose_name="Engineer Surname")
    aircraft_types = models.ManyToManyField('AircraftType', related_name='aircraft_types', blank=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    """
    Model for engineer's work with aircraft.
    """
    objects = WorkQuerySet.as_manager()

    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Work Date")
    status = models.CharField(max_length=255, choices=[
        ('WORKING', 'Working'),
        ('VACATION', 'Vacation'),
        ('SICK_LEAVE', 'Sick Leave'),
    ], default='WORKING', verbose_name="Work Status")
    mh = models.IntegerField(default=7, verbose_name="MH")

    class Meta:
        unique_together = ('engineer', 'aircraft', 'date')

    def __str__(self):
        return f"{self.engineer.name} - {self.aircraft.aircraft_type.type} - {self.date}"

    @property
    def stred_date(self):
        return self.date.strftime('%Y-%m-%d')
