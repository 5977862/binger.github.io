from django.db import models
from mysite.settings import HOME_PER_LINE_LENGTH

# Create your models here.
class news(models.Model):
    title = models.TextField()
    body = models.TextField()

    def getTitlesForHome(self):
        linenum = HOME_PER_LINE_LENGTH
        title_list = []
        title_list.append(self.id)
        if len(self.title) > linenum:
            title_list.append(self.title[:linenum] + ' ...')
        else:
            title_list.append(self.title[:linenum])
        return title_list
    
    def __unicode__(self):
        return self.title