from django.db import models



# Create your models here.
class Aircraft(models.Model):
    tail_number = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=50)
    aircraft_type = models.CharField(max_length=100)
    year_of_production = models.CharField(max_length=10)
    photo1 = models.URLField(null=True, blank=True)
    photo2 = models.URLField(null=True, blank=True)
    photo3 = models.URLField(null=True, blank=True)


