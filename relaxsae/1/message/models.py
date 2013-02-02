#-*- coding:utf-8 -*-
from django.db import models
from userinfo.models import Userinfo

# Create your models here.
class Message(models.Model):
    title = models.CharField(max_length = 30)
    body = models.TextField()
    state = models.IntegerField()
    date = models.DateTimeField()
    user_from = models.ForeignKey(Userinfo,related_name='user_from')
    user_to = models.ForeignKey(Userinfo,related_name='user_to')

    def getTitle(self):
        ret_str = ''
        if len(self.title) > 10:
            ret_str ='%s%s' % (self.title[:10],'...')
        else:
            ret_str = self.title
        return ret_str