#-*- coding:utf-8 -*-
'''
Created on 2013-1-21

@author: Binger
'''

from django.db import models
from userinfo.models import Userinfo

class base_project_model(models.Model):
    username = models.ForeignKey(Userinfo)
    title = models.TextField()
    body = models.TextField()
    date = models.DateTimeField()
    count = models.IntegerField()
    last_date = models.DateTimeField()

    def getTitle(self):
        count = 0
        index = 0
        title = self.title
        length = len(title)
        while index < length:
            try:
                len(title[index].decode('utf-8'))
                count += 1
            except:
                count += 2
            index += 1
            if count > 90 and index < length:
                break
        else:
            return title
            
        return '%s ...' % title[:index]

    def getTitleForHome(self):
        linenum = 23
        title_list = []
        title_list.append(self.id)
        if len(self.title) > linenum:
            title_list.append(self.title[0:linenum] + ' ...')
        else:
            title_list.append(self.title)
        return title_list

    def __unicode__(self):
        return self.title
    
    class Meta:
        abstract = True
        
class base_relation_model(models.Model):
    username = models.ForeignKey(Userinfo)
    date = models.DateTimeField()
    text = models.TextField()
    
    class Meta:
        abstract = True