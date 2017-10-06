from django.db import models



# Create your models here.
class Location(models.Model):
    building_name = models.CharField(max_length=50)
    building_address = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)

class Student(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    @classmethod
    def create(cls, name, year):
        student = cls(name=name, year=year)
        return student

class Group(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    loc = models.ForeignKey('Location',
                            on_delete=models.CASCADE,
                            null=True)
    @classmethod
    def create(cls, name, size):
        group = cls(name=name, size=size)
        return group
    students = models.ManyToManyField(Student)
