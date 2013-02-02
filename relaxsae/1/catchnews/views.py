#-*- coding:gb2312 -*-

from sgmllib import SGMLParser
import urllib2
from news.models import news
import threading
from django.http import HttpResponseRedirect

def catch_news_action(request):
    username = request.session.get('user','')
    if username == 'admin':
        thread_new = thread_news(True)
        thread_new.start()
    return HttpResponseRedirect('/home')
    
class thread_news(threading.Thread):
    def __init__(self,flag):
        threading.Thread.__init__(self)
        self.flag = flag
    def run(self):
        if self.flag:
            domain()
        
    def stop(self):
        pass


class GetUrl(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.is_a = 0
        self.href = []
        self.newurl = "http://news.qq.com/a/"
        
    def start_a(self,attrs):
        hrefs = [j for i,j in attrs if i == 'href']
        for i in hrefs:
            if self.newurl in i and "#" not in i:
                self.href.append(i)
        
    def end_h1(self):
        self.is_a = 0
        
    def handle_data(self,text):
        pass


def getInfo(url):
    text = urllib2.urlopen(url).read()
    find = finder()
    find.feed(text)
    title = ""
    body = ""
    for item in find.title:
        title = item
    for item in find.body:
        body += item
    insertin(title,body)
 
def dofind(hreflist):
    for i in hreflist:
        getInfo(i)
        

class finder(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.is_h1 = False
        self.is_p = False
        self.is_return = False
        self.is_right = True
        self.is_span = True
        self.title = []
        self.body = []
        
    def start_h1(self,attrs):
        self.is_h1 = True
        
    def end_h1(self):
        self.is_h1 = False
        
    def start_p(self,attrs):
        self.is_p = True
        
    def end_p(self):
        self.is_p = False
        
    def start_span(self,attrs):
        if self.is_right != False:            
            self.is_right = False
            self.is_span = False
        
    def end_span(self):
        if self.is_span == False:
            self.is_right = True
            self.is_span = True
        
    def start_li(self,attrs):
        self.is_right = False
        
    def end_li(self):
        self.is_right = True
    
    def start_style(self,attrs):
        self.is_right = False
        
    def end_style(self):
        self.is_right = True
    
    def start_script(self,attrs):
        self.is_right = False
        
    def end_script(self):
        self.is_right = True
    
    def start_b(self,attrs):
        self.is_right = False
        
    def end_b(self):
        self.is_right = True
    
    def start_h2(self,attrs):
        self.is_right = False
        
    def end_h2(self):
        self.is_right = True
    
    def start_a(self,attrs):
        self.is_right = False
        
    def end_a(self):
        self.is_right = True
    
    def start_label(self,attrs):
        self.is_right = False
        
    def end_label(self):
        self.is_right = True
        
    def start_button(self,attrs):
        self.is_right = False
        
    def end_button(self):
        self.is_right = True
    
    def handle_data(self,text):
        if self.is_return:
            return
        if self.is_h1:
            self.title.append(text)
        if self.is_p and self.is_right:
            if not self.__badline(text):
                self.body.append(text.strip()+'<cut>')
        
    def __badline(self,text):
        if (');' in text) or ('document.write' in text) or ('document.write' in text) or ('All Rights Reserved' in text) or ('data.hot_list[i].reply_content' in text):
            return True
        return False
    
class GetUrlLink(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.href = []
        self.newurl = "http://news.qq.com/a/"
        
    def start_a(self,attrs):
        hrefs = [j for i,j in attrs if i == 'href']
        for i in hrefs:
            if self.newurl in i and "#" not in i:
                self.href.append(i)
        
def insertin(title,body):
    if "组图" not in title and "高清" not in title:
        new = news(title = title.decode('gb2312').encode('utf8'),body = body.decode('gb2312').encode('utf8'))
        new.save()
            
def domain():
    context = urllib2.urlopen("http://news.qq.com/").read()
    f = GetUrlLink()
    f.feed(context)
    hreflist = []
    for i in f.href:
        for j in i.split():
            if len(j.strip()) > 21:
                hreflist.append(j)
    hreflist = list(set(hreflist))
    dofind(hreflist)