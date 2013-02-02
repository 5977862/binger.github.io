#-*- coding:utf-8 -*-
from userinfo.models import Userinfo
from django.contrib import auth
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from userinfo.forms import Userform,Usereditform
import smtplib
from email.mime.text import MIMEText
from email.Header import Header
import time,md5,sha,random
from mysite.settings import WEB_SERVER_HOST,NEW_USER_TITLE,NEW_USER_BODY
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from message.models import Message
from django.contrib.auth.forms import UserCreationForm

def put_user_and_msg_count(func):
    def _put_user_and_msg_count(*argvs):
        username = argvs[0].session.get('user',False)
        msg_count = get_msg_count(username)
        ret_argvs = list(argvs)
        ret_argvs.append(username)
        ret_argvs.append(msg_count)
        return func(*ret_argvs)
    return _put_user_and_msg_count

@put_user_and_msg_count
def success_action(request,username=False,msg_count=0):
    success_msg = request.GET.get('msg','')
    return render_to_response('success.html',locals())

@put_user_and_msg_count
def error_action(request,username=False,msg_count=0):
    error_msg = request.GET.get('msg','')
    return render_to_response('error.html',locals())

@login_required
@put_user_and_msg_count
def userinfo_action(request,username=False,msg_count=0):
    userinfo = Userinfo.objects.get(username=username)
    form = Userform()
    return render_to_response('user.html', locals())

def regiest_action(request):
    if request.method == "POST":
        userform = Userform(request.POST)
        msg_count = 1
        if userform.is_valid():
            userform = userform.cleaned_data
            t_username = userform.get('username')
            user = UserCreationForm({'username':t_username,'password1':userform.get('passwd1'),'password2':userform.get('passwd2')})
            verify = getverify()
            ret = send(userform.get('email'), t_username, verify)
            if ret:
                username = t_username
                user.save()
                userinfo = Userinfo(username=userform.get('username'),activity='0',email=userform.get('email'),telephone=userform.get('telephone'),address=userform.get('address'),verify=security(verify),gender=userform.get('gender'),id=User.objects.get(username = username))
                userinfo.save()
                user = auth.authenticate(username = username,password = userform.get('passwd1'))
                auth.login(request,user)
                request.session['user'] = username
                user_from = Userinfo.objects.get(username = 'admin')
                user_to = Userinfo.objects.get(username = username)
                message = Message(title  = NEW_USER_TITLE,body = NEW_USER_BODY,state = 0,date = datetime.now(),user_from = user_from,user_to = user_to)
                message.save()
                success_msg = '请登录%s查收邮件激活！'.decode('utf-8')  % userform.get('email')
                return jump_to_success(success_msg)
            else:
                error_msg = '验证邮件发送失败！'
                return jump_to_error(error_msg)
            
        else:
            error = "出错了，请重新注册！"
            return render_to_response('regiest.html',locals())
    else:
        return render_to_response('regiest.html',locals())

@login_required
@put_user_and_msg_count
def userinfo_submit_action(request,username=False,msg_count=0):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            form_cd = form.cleaned_data
            verify = getverify()
            ret = send(form_cd.get('email'), username, verify)
            if ret:
                Userinfo.objects.filter(username=username).update(gender=form_cd.get('gender'), email=form_cd.get('email'), telephone=form_cd.get('telephone'), address=form_cd.get('address'),verify=security(verify))
                success_msg = '请查收邮件激活！'
                return jump_to_success(success_msg)
            else:
                error_msg = '验证邮件发送失败！'
                return jump_to_error(error_msg)
        else:
            error = True
            form = Userform()
            return render_to_response('user.html',locals())
    return HttpResponseRedirect('/home')

def activity_action(request):
    if request.method == 'GET':
        t_username = request.GET.get('username','')
        verify = request.GET.get('verify','')
        try:
            user = Userinfo.objects.get(username = t_username)
        except:
            error_msg = '没有注册信息，或已经注册过了！'
            return jump_to_error(error_msg)
            
        ret = Userinfo.objects.filter(username = user,verify = security(verify),activity='0')
        if len(ret):
            ret.update(activity='1',verify='')
            success_msg = '激活成功！'
            return jump_to_success(success_msg)
        else:
            error_msg = '没有注册信息，或已经注册过了！'
            return jump_to_error(error_msg)
        
@login_required
@put_user_and_msg_count
def edit_user_action(request,username=False,msg_count=0):
    userinfo = Userinfo.objects.get(username = username)
    form = Usereditform()
    if request.method == 'POST':
        form = Usereditform(request.POST)
        if form.is_valid():
            form_cd = form.cleaned_data
            t_mail = form_cd.get('email')
            if userinfo.email == t_mail:
                Userinfo.objects.filter(username=username).update(telephone=form_cd.get('telephone'), address=form_cd.get('address'))
                success_msg = '修改成功！'
                return jump_to_success(success_msg)
            else:
                verify = getverify()
                if send(form_cd.get('email'), username, verify):
                    Userinfo.objects.filter(username=username).update(email=form_cd.get('email'), telephone=form_cd.get('telephone'), address=form_cd.get('address'),verify=security(verify),activity='0')                
                    success_msg = '您修改了邮箱，请登录邮箱重新激活！'
                    return jump_to_success(success_msg)
                else:
                    error_msg = '验证邮件发送失败，请返回再试一次！'
                    return jump_to_error(error_msg)
        else:
            error = "填写错误，请重新填写！"
            return render_to_response('edit.html',locals())
    else:
        return render_to_response('edit.html',locals())

def forget_passwd_action(request):
    if request.method == 'POST':
        t_username = request.POST.get('username',0)
        email = request.POST.get('email',0)
        if not t_username or not email:
            error = '不能有空白项！'
            return render_to_response('forget_passwd.html',locals())
        try:
            Userinfo.objects.get(username = t_username,email = email)
        except:
            error = '该邮箱与用户不匹配！'
            return render_to_response('forget_passwd.html',locals())
        verify = getverify()
        Userinfo.objects.filter(username = t_username,email = email).update(verify = verify)
        if send(email, t_username, verify, 'getpasswd'):
            success_msg = '请登录邮箱重置密码'
            return jump_to_success(success_msg)
        else:
            error_msg = '验证邮件发送失败，请返回再试一次！'
            return jump_to_error(error_msg)
    else:
        return render_to_response('forget_passwd.html',locals())

def getpasswd_action(request):
    if request.method == 'POST':
        t_username = request.POST.get('username',0)
        passwd1 = request.POST.get('passwd1',0)
        passwd2 = request.POST.get('passwd2',0)
        if not t_username or passwd1 != passwd2 or not passwd1:
            error = '两次密码输入不一致！'
            return render_to_response('getpasswd.html',locals())
        user = User.objects.get(username = t_username)
        user.set_password(passwd1)
        user.save()
        success_msg = '密码设置成功！'
        return jump_to_success(success_msg)
    else:
        t_username = request.GET.get('username',0)
        verify = request.GET.get('verify',0)
        try:
            Userinfo.objects.get(username = t_username,verify = verify)
        except:
            error_msg = '错误的链接！'
            return jump_to_error(error_msg)
        return render_to_response('getpasswd.html',locals())

def getverify():
    return '%s%s' % (time.time(),random.randrange(999999999))

def security(m_str):
    md5_value = md5.new(m_str).hexdigest()
    return sha.new(md5_value).hexdigest()

def send(send_to,username,verify,activity='activity'):
    try:
        char_set = 'utf-8'
        title = ''
        if activity == "activity":
            title = '注册激活'
        else:
            title = '找回密码'
        activity_link = 'http://%s/%s?username=%s&verify=%s' % (WEB_SERVER_HOST,activity,username,verify)
        words = ""
        if activity == "activity":
            words = " 感谢您的注册，请点击下面链接激活您的账号！"
        else:
            words = " 感谢您的使用，请点击下面链接重置您的密码！"
        text = '''
        你好，%s
        
           %s
    %s
    
    此邮件为系统发送，请勿回复！
        '''.decode(char_set) % (username,words.decode(char_set),activity_link)
        message = MIMEText(text,_charset = char_set)
        message['subject'] = Header(title,char_set)
        message['from'] = 'relax-activity@qq.com'
        message['to'] = send_to
        message['text'] = text
        smtp = smtplib.SMTP("smtp.qq.com:25")
        smtp.login("relax-activity","jiangdebin")
        smtp.sendmail("relax-activity@qq.com",send_to,message.as_string())
        smtp.quit()
        return True
    except Exception:
        return False

def get_msg_count(username):
    if username == 0 or username == '':
        return 0
    try:
        user = Userinfo.objects.get(username = username)
    except:
        return 0
    return Message.objects.filter(user_to = user,state = 0).count()

def jump_to_success(msg):
    return HttpResponseRedirect('/success?msg=%s' % msg)

def jump_to_error(msg):
    return HttpResponseRedirect('/error?msg=%s' % msg)

def get_page(page,type,perpage,objs):
    try:
        page = int(page)
    except:
        page = 1
    if type == 'next':
        page = page + 1
    if type == 'previous':
        page = page - 1
    pages = len(objs)/perpage + int(len(objs)%perpage > 0)
    if page > pages:
        page = pages
    if page == 0:
        page = 1
    return page,pages