#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from models import news
from userinfo.views import get_msg_count, get_page, put_user_and_msg_count

@put_user_and_msg_count
def news_action(request,sign,username=False,msg_count=0):
    empty = False
    perpage = 20
    page = request.GET.get('page','1')
    type = request.GET.get('type','')
    news_all = news.objects.all()
    page,pages = get_page(page, type, perpage, news_all)
    if len(news_all) > 0:
        news_all = news_all[(page-1)*perpage:page*perpage]
    else:
        empty = True
    page_url = 'news'
    return render_to_response('news.html',locals())

@put_user_and_msg_count
def news_single_action(request,sign,no,username=False,msg_count=0):
    words = 60
    try:
        new = news.objects.get(id = int(no))
    except :
        pass
    title = new.title
    body = new.body
    bodylist = body.split('<cut>')
    return render_to_response('new_single.html',locals())