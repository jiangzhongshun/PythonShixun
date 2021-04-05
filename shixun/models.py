from django.db import models

# Create your models here.
from django.db import models

class user(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class movies(models.Model):
    movieName=models.CharField(max_length=20)
    movieActor=models.CharField(max_length=20)
    movieTime=models.CharField(max_length=20)
    movieGrade=models.CharField(max_length=20)

class goods(models.Model):
    goodName=models.CharField(max_length=30)
    goodLink=models.CharField(max_length=20)
    goodPrice=models.CharField(max_length=20)
    goodGrade=models.CharField(max_length=20)