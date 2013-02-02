#-*- coding:utf-8 -*-
'''
Created on 2012-11-26

@author: Binger
'''
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from items.models import Problem_Relation,Relax_Relation,Tutsau_Relation,Relax,Problem,Tutsau
from datetime import datetime
from news.models import news
from userinfo.models import Userinfo
from mysite.settings import HOME_ITEM_LINES,VAR_DICT
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from userinfo.views import jump_to_error, jump_to_success,get_msg_count,\
    put_user_and_msg_count

def home_action(request):
    sign = 'home'
    linenum = HOME_ITEM_LINES
    username = request.session.get('user','')
    msg_count = get_msg_count(username)
    new = news.objects.all()[:23]
    problems = Problem.objects.all()[:linenum]
    relaxs = Relax.objects.all()[:linenum]
    tutsaus = Tutsau.objects.all()[:linenum]
    
    home_btn = VAR_DICT['HOME_BTN_VALUE']
    home_title = VAR_DICT['HOME_TITLE_VALUE']
    home_body = VAR_DICT['HOME_BODY_VALUE']
    home_img_url = VAR_DICT['HOME_IMG_URL']
    
    ifoundyou_btn = VAR_DICT['IFOUNDYOU_BTN_VALUE']
    ifoundyou_title = VAR_DICT['IFOUNDYOU_TITLE_VALUE']
    ifoundyou_body = VAR_DICT['IFOUNDYOU_BODY_VALUE']
    ifoundyou_btn_link = VAR_DICT['IFOUNDYOU_BTN_LINK']
    ifoundyou_img_url = VAR_DICT['IFOUNDYOU_IMG_URL']
    
    problem_btn = VAR_DICT['PROBLEM_BTN_VALUE']
    problem_title = VAR_DICT['PROBLEM_TITLE_VALUE']
    problem_body = VAR_DICT['PROBLEM_BODY_VALUE']
    problem_img_url = VAR_DICT['PROBLEM_IMG_URL']
    
    relax_btn = VAR_DICT['RELAX_BTN_VALUE']
    relax_title = VAR_DICT['RELAX_TITLE_VALUE']
    relax_body = VAR_DICT['RELAX_BODY_VALUE']
    relax_img_url = VAR_DICT['RELAX_IMG_URL']
    
    tutsau_btn = VAR_DICT['TUTSAU_BTN_VALUE']
    tutsau_title = VAR_DICT['TUTSAU_TITLE_VALUE']
    tutsau_body = VAR_DICT['TUTSAU_BODY_VALUE']
    tutsau_img_url = VAR_DICT['TUTSAU_IMG_URL']
    
    return render_to_response("home.html",locals())

def checkuser_action(request):
    t_username = request.GET.get('username',False)
    if t_username:
        try:
            User.objects.get(username = t_username)
            return HttpResponse('exist')
        except:
            return HttpResponse('ok')
    else:
        return HttpResponse('error')

def login_action(request):
    if request.method == 'POST':
        m_username = request.POST.get("username","")
        passwd = request.POST.get("passwd","")
        next = request.POST.get('next','')
        user = auth.authenticate(username = m_username,password = passwd)
        if not user:
            error = "用户名或密码错误"
            return render_to_response("login_required.html",locals())
        auth.login(request,user)
        request.session['user'] = m_username
        username = m_username
        msg_count = get_msg_count(username)
        if next != '':
            if next.startswith('/submitwords'):
                next = '%s%s' % ('/',next[13:])
            return HttpResponseRedirect(next)
        return render_to_response("logined.html",locals())
    
    else:
        next = request.GET.get('next','')
        return render_to_response("login_required.html",locals())

@login_required
@put_user_and_msg_count
def submit_words_action(request,username=False,msg_count=0):
    if request.method == "POST":
        user_instance = Userinfo.objects.get(username = username)
        url = request.POST.get('type','')
        title_id = request.POST.get('title_id','')
        t_text = request.POST.get('text','')
        
        if t_text:
            obj_name = url[13:].capitalize()
            obj = globals()[obj_name]
            try:
                title_instance = obj.objects.get(id = title_id)
            except:
                error_msg = '此帖已不存在！'
                return jump_to_error(error_msg)
            obj.objects.filter(id = title_id).update(last_date = datetime.now(),count = title_instance.count + 1)
            relation = globals()['%s_Relation' % obj_name](username = user_instance,title = title_instance,text = t_text,date = datetime.now())
            relation.save()
    return HttpResponseRedirect('/%s?id=%s&tolow=1&page=99999' % (url,title_id))

@login_required
@put_user_and_msg_count
def change_password_action(request,username=False,msg_count=0):
    userinfo = Userinfo.objects.get(username=username)
    activity = userinfo.activity
    if request.method == "POST":
        original_passwd = request.POST.get('original_passwd','')
        passwd1 = request.POST.get('passwd1','')
        passwd2 = request.POST.get('passwd2','')
        if passwd1 == passwd2:
            if len(passwd1) < 6:
                error = '新密码不能少于6位！'
                return render_to_response('changepasswd.html',locals())            
            user = auth.authenticate(username = username,password = original_passwd)
            if user:
                user = User.objects.get(username = username)
                user.set_password(passwd1)
                user.save()
                success_msg = '密码修改成功！'
                return jump_to_success(success_msg)
            else:
                error = '原密码错误！'
                return render_to_response('changepasswd.html',locals())
        else:
            error = '两次新密码不同！'
            return render_to_response('changepasswd.html',locals())
    else:
        return render_to_response('changepasswd.html',locals())