from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Userinfo(models.Model):
    id = models.ForeignKey(User)
    username = models.CharField(max_length=30,unique=True,primary_key = True)
    gender = models.CharField(max_length=7)
    email = models.CharField(max_length=40)
    activity = models.CharField(max_length=2)
    telephone = models.CharField(max_length=15)
    address = models.CharField(max_length=80,blank=True,null=True)
    verify = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username