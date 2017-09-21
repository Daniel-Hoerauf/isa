from django.db import models



# Create your models here.
class Location(models.Model):
    building_name = models.CharField(max_length = 50)
    building_address = models.CharField(max_length = 50)
    College_name = models.CharField(max_length = 50)
    
class Students(models.Model):
    name = models.CharField()
    year = models.IntegerField()

class Groups(models.Model):
    size = models.IntegerField()
    