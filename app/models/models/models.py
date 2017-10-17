from datetime import datetime, timedelta
from django.db import models



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
    description = models.CharField(max_length=100, default='Come and learn!')
    loc = models.ForeignKey(Location,
                            on_delete=models.CASCADE,
                            null=True)
    students = models.ManyToManyField(Student)

    @classmethod
    def create(cls, name, size, description):
        if description is None:
            group = cls(name=name, size=size)
        else:
            group = cls(name=name, size=size, description=description)
        return group


class User(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    password = models.CharField(max_length=1000)


class Authenticator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authenticator = models.CharField(max_length=1000, primary_key=True)
    date_created = models.DateTimeField(auto_now=True)


def clean_authenticators(authenticator):
    expired_date = datetime.now() - timedelta(hours=8)
    old_auths = Authenticator.objects.filter(date_created__lte=expired_date)
    for auth in old_auths:
        auth.delete()
