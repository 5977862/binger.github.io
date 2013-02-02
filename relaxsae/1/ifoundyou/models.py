from django.db import models
from userinfo.models import Userinfo

# Create your models here.
class Coordinate(models.Model):
    username = models.ForeignKey(Userinfo)
    telephone = models.CharField(max_length = 16)
    times = models.CharField(max_length = 60,primary_key = True)
    now_time = models.CharField(max_length = 28)
    passwd = models.CharField(max_length = 42)
    
    def __unicode__(self):
        return self.times

class CoordinateTimes(models.Model):
    times = models.ForeignKey(Coordinate)
    current_time = models.DateTimeField()
    longitude = models.CharField(max_length = 20)
    latitude = models.CharField(max_length = 20)