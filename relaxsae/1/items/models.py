#-*- coding:utf-8 -*-
from django.db import models
from userinfo.models import Userinfo
from basemodel import base_project_model,base_relation_model

# Create your models here.
class Problem(base_project_model):
    pass

class Problem_Relation(base_relation_model):
    title = models.ForeignKey(Problem)

class Tutsau(base_project_model):
    pass

class Tutsau_Relation(base_relation_model):
    title = models.ForeignKey(Tutsau)
    
class Relax(base_project_model):
    pass
    
class Relax_Relation(base_relation_model):
    title = models.ForeignKey(Relax)

    
class JoinUs(models.Model):
    username = models.ForeignKey(Userinfo)
    title = models.ForeignKey(Relax)
    date = models.DateTimeField()
        