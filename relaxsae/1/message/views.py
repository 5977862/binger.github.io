#-*- coding:utf-8 -*-
from userinfo.views import jump_to_error, put_user_and_msg_count
from message.models import Message
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime
from userinfo.models import Userinfo
from userinfo.views import get_msg_count
from django.contrib.auth.decorators import login_required

@put_user_and_msg_count
def message_action(request,username=False,msg_count=0):
    messages = Message.objects.filter(user_to = username)
    return render_to_response('message.html',locals())

@login_required
@put_user_and_msg_count
def single_message_action(request,num,username=False,msg_count=0):
    if request.method == 'GET':
        Message.objects.filter(id=num).update(state=1)
        user_to = Userinfo.objects.get(username = username)
        try:
            message = Message.objects.get(id = num,user_to = user_to)
        except Message.DoesNotExist:
            error_msg = '出错了，请返回！'
            return jump_to_error(error_msg)
        return render_to_response('single_message.html',locals())

@login_required
def delete_message_action(request,num):
    username = request.session.get('user','')
    try:
        user = Userinfo.objects.get(username = username)
    except:
        jump_to_error("请重新删除！")
    if request.method == 'GET':
        Message.objects.filter(id=num,user_to = user).delete()
        return HttpResponseRedirect('/message')

@login_required
@put_user_and_msg_count
def new_message_action(request,send_to,username=False,msg_count=0):
    if request.method == 'GET':
        return render_to_response('new_message.html',locals())
    elif request.method == 'POST':
        send_to = request.POST.get('send_to','')
        title = request.POST.get('title','')
        body = request.POST.get('body','')
        if len(send_to) == 0 or len(title) == 0 or len(body) == 0:
            error = '不能有空白项'
            return render_to_response('new_message.html',locals())
        else:
            user = Userinfo.objects.get(username = username)
            try:
                send_to = Userinfo.objects.get(username = send_to)
            except:
                error = '不存在用户： %s'.decode('utf-8') % send_to
                send_to = ''
                return render_to_response('new_message.html',locals())
            message = Message(title = title,body = body,state = 0,date = datetime.now() ,user_from = user,user_to = send_to)
            message.save()
            return HttpResponseRedirect('/message')