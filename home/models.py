from django.db import models



# Create your models here.
class Location(models.Model):
    building_name = models.CharField(max_length=50)
    building_address = models.CharField(max_length=50)
    College_name = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField()
    year = models.IntegerField()

class Group(models.Model):
    size = models.IntegerField()
    loc = models.ForeignKey('Location',
                            on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
