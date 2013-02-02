#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from items.models import *
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from mysite.settings import MAIN_PAGE_PER_PAGE_LINES,VAR_DICT, FORUM_LIST
from django.contrib.auth.decorators import login_required
from userinfo.views import jump_to_error,get_msg_count,get_page,\
    put_user_and_msg_count

def check_sign(func):
    def _check_func(*argvs):
        if argvs[1] not in FORUM_LIST:
            return HttpResponseRedirect('/home')
        else:
            return func(*argvs)
    return _check_func

@check_sign
@put_user_and_msg_count
def item_action(request,sign,username=False,msg_count=0):
    instance=str(sign).capitalize()
    new_link='/forum/new_%s' % sign
    link='/forum/single_%s' % sign
    btn = VAR_DICT['%s_BTN_VALUE' % str(sign).upper()]
    title= VAR_DICT['%s_TITLE_VALUE' % str(sign).upper()]
    body=VAR_DICT['%s_BODY_VALUE' % str(sign).upper()]
    
    perpage = MAIN_PAGE_PER_PAGE_LINES
    mine = request.GET.get('mine','')
    type = request.GET.get('type','')
    page = request.GET.get('page','1')
    img_url = VAR_DICT['%s_IMG_URL' % str(sign).upper()]
    if mine:
        try:
            user = Userinfo.objects.get(username = username)
        except:
            return HttpResponseRedirect("/login?next=/forum/%s?mine=1" % sign)
        objs = globals()[instance].objects.filter(username = user).order_by('-last_date')
    else:
        objs = globals()[instance].objects.all().order_by('-last_date')
        
    page,pages = get_page(page, type, perpage, objs)
        
    if len(objs) > 0:
        objs = objs[(page-1)*perpage:page*perpage]
    else:
        empty = True
    page_url = 'forum/%s' % sign
    return render_to_response('itemlist.html',locals())

@check_sign
@put_user_and_msg_count
def item_new_action(request,sign,username=False,msg_count=0):
    action='add_%s' % sign
    return render_to_response('add_new.html',locals())

@login_required
@check_sign
@put_user_and_msg_count
def add_item_action(request,sign,username=False,msg_count=0):
    instance=str(sign).capitalize()
    action='add_%s' % sign
    user_instance = Userinfo.objects.get(username = username)
    if request.method == "POST":
        t_title = request.POST.get("title","")
        t_body = request.POST.get("body","")
        if t_title.strip() != "" and t_body.strip() != "":
            t_now = datetime.now()
            obj = globals()[instance](username = user_instance,title = t_title,body = t_body,date = t_now,last_date = t_now,count = 0)
            obj.save()
            if instance == 'Relax':
                user_instance = Userinfo.objects.get(username = username)
                join = JoinUs(username = user_instance,title = obj,date = datetime.now())
                join.save()
            return HttpResponseRedirect('/forum/single_%s?id=%s' % (sign,obj.id))
        else:
            error = "不能有空白项"
            return render_to_response('add_new.html',locals())
    else:
        return render_to_response('add_new.html',locals())
        
@check_sign
@put_user_and_msg_count
def single_item_action(request,sign,username=False,msg_count=0):
    instance=str(sign).capitalize()
    relat_instance='%s_Relation' % instance
    url='forum/single_%s' % sign
    canjoin = sign == 'relax'
    
    if request.method == "GET":
        type = request.GET.get('type','')
        page = request.GET.get('page','1')
        t_id = request.GET.get("id")
        tolow = request.GET.get("tolow",'')
        perpage = 5
        try:
            obj = globals()[instance].objects.get(id = t_id)
        except:
            error_msg = '出错了，返回再试试吧！'
            return jump_to_error(error_msg)
        relations = globals()[relat_instance].objects.filter(title_id = obj.id)
        page,pages = get_page(page,type,perpage,relations)
        if len(relations) > 0:
            relations = relations[(page-1)*perpage:page*perpage]
        else:
            empty = True
            page = 1
        if canjoin:
            try:
                joinus = JoinUs.objects.get(title_id = t_id,username = username)
                joined = True
                datetime = joinus.date
            except:
                joined = False
        page_url = 'forum/single_%s' % sign
        return render_to_response('single.html',locals())

@login_required
@put_user_and_msg_count
def join_action(request,username=False,msg_count=0):
    sign = 'relax'
    if request.method == 'POST':
        id = request.POST.get('id','')
        join = JoinUs.objects.filter(username = username,title_id = id)
        if len(join):
            return HttpResponse('已经参加')
        else:
            relax = Relax.objects.filter(id = id)
            if len(relax):
                user_instance = Userinfo.objects.get(username = username)
                title_instance = Relax.objects.get(id = id)
                join = JoinUs(username = user_instance,title = title_instance,date = datetime.now())
                join.save()
                return HttpResponse('参加成功')
            else:
                return HttpResponse('出问题')

@put_user_and_msg_count
def joined_action(request,username=False,msg_count=0):
    sign = 'relax'
    if request.method == 'GET':
        t_id = request.GET.get('id',False)
        if t_id:
            try:
                relax = Relax.objects.get(id = t_id)
            except:
                return HttpResponseRedirect('/forum/relax')
            if username != relax.username.username:
                error_msg = "只有发起者才能查看！"
                return jump_to_error(error_msg)
            joins = JoinUs.objects.filter(title = relax)
            empty = len(joins) == 0
            return render_to_response('join.html',locals())
