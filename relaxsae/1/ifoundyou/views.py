#-*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from userinfo.models import Userinfo
from ifoundyou.models import Coordinate, CoordinateTimes
from django.shortcuts import render_to_response
from mysite.settings import ANDROID_CLIENT_VERSION,VAR_DICT
from django.contrib.auth.decorators import login_required
from userinfo.views import security, jump_to_error,get_msg_count,\
    put_user_and_msg_count

def ifoundyou_set_permission_action(request):
    if request.method == 'POST':
        telephone = request.POST.get('telephone','')
        times = request.POST.get('times','')
        passwd = request.POST.get('passwd','')
        try:
            Coordinate.objects.get(telephone = telephone,times = times,passwd = security(passwd))
            request.session['%s%s' % (telephone,times)] = True
            return HttpResponse('ok')
        except:
            return HttpResponse('error')
    else:
        return HttpResponseRedirect('/home')

@login_required
@put_user_and_msg_count
def ifoundyou_by_time(request,sign,username=False,msg_count=0):
    if request.method == 'GET':
        index_time = request.GET.get('index_time','')
        telephone = request.GET.get('telephone','')
        if not index_time or not telephone:
            error_msg = '出错了'
            return jump_to_error(error_msg)
        else:
            coordinates = Coordinate.objects.filter(telephone = telephone).order_by('-now_time')
            try:
                get_coordinate = Coordinate.objects.get(telephone = telephone,now_time = index_time)
                times = get_coordinate.times
                ispasswded = request.session.get('%s%s' % (telephone,times),False)
                date = get_coordinate.now_time
                if not ispasswded:
                    return render_to_response('ifoundyou_res.html',locals())
                coordinatetimes = CoordinateTimes.objects.filter(times = get_coordinate.times)
            except:
                error_msg = '没有要查找的信息'
                return jump_to_error(error_msg)
            type,longitude,latitude,t_time = get_map_src(coordinatetimes)
            return render_to_response('ifoundyou_res.html',locals())

@login_required
@put_user_and_msg_count
def ifoundyou_by_phone(request,sign,username=False,msg_count=0):
    title = VAR_DICT['IFOUNDYOU_TITLE_VALUE']
    btn = VAR_DICT['IFOUNDYOU_BTN_VALUE']
    body = VAR_DICT['IFOUNDYOU_BODY_VALUE']
    if request.method == 'POST':
        telephone = request.POST.get('telephone','')
        if telephone.startswith('+86'):
            telephone = telephone[3:]
        elif telephone.startswith('0086'):
            telephone = telephone[4:]
        elif len(telephone) != 11 or telephone[0] != '1':
            error = '手机号码错误！'
            return render_to_response('ifoundyou.html',locals())
        try:
            int(telephone)
        except:
            error = '手机号码错误！'
            return render_to_response('ifoundyou.html',locals())
        coordinates = Coordinate.objects.filter(telephone = telephone).order_by('-now_time')
        if(len(coordinates) == 0):
            error = "没有该号码的定位信息！"
            return render_to_response('ifoundyou.html',locals())
        if len(coordinates) == 0:
            empty = True
        else:
            index_time = coordinates[0].now_time
        times = coordinates[0].times
        ispasswded = request.session.get('%s%s' % (telephone,times),False)
        date = coordinates[0].now_time
        if not ispasswded:
            return render_to_response('ifoundyou_res.html',locals())
        coordinatetimes = CoordinateTimes.objects.filter(times = coordinates[0].times)
        type,longitude,latitude,t_time = get_map_src(coordinatetimes)
        return render_to_response('ifoundyou_res.html',locals())
    else:
        return render_to_response('ifoundyou.html',locals())
    
@put_user_and_msg_count
def ifoundyou_action(request,sign='',username=False,msg_count=0):
    title = VAR_DICT['IFOUNDYOU_TITLE_VALUE']
    btn = VAR_DICT['IFOUNDYOU_BTN_VALUE']
    body = VAR_DICT['IFOUNDYOU_BODY_VALUE']
    link = VAR_DICT['IFOUNDYOU_BTN_LINK']
    img_url = VAR_DICT['IFOUNDYOU_IMG_URL']
    return render_to_response('ifoundyou.html',locals())

def getcoordinate_action(request):
    username = request.GET.get('username',0)
    passwd = request.GET.get('passwd',0)
    telephone = request.GET.get('telephone',0)
    times = request.GET.get('times',0)
    longitude = request.GET.get('longitude',0)
    latitude = request.GET.get('latitude',0)
    version = request.GET.get('version',0)
    
    if not username or not telephone or not times or not longitude or not latitude or not passwd or not version:
        return HttpResponse('parameter error')
    else:
        if version < ANDROID_CLIENT_VERSION:
            return HttpResponse("update")
        try:
            Userinfo.objects.get(username=username)
        except:
            return HttpResponse("user doesn't exist")
        if len(passwd) == 0:
            return HttpResponse('passwd length error')
        if telephone.startswith('+86'):
            telephone = telephone[3:]
        elif telephone.startswith('0086'):
            telephone = telephone[4:]
        elif telephone[0] != '1':
            return HttpResponse('telephone error')
        try:
            int(telephone)
        except:
            return HttpResponse('telephone error just num')
        try:
            pass
            longitude = str(float(longitude))
            latitude = str(float(latitude))
        except:
            return HttpResponse('longitude or latitude is error')
        user = Userinfo.objects.get(username = username)
        try:
            coordinate = Coordinate.objects.get(username = username,telephone = telephone,times = '%s%s' % (username,times))
        except:
            coordinate = Coordinate(username = user,passwd = security(passwd),telephone = telephone,times = '%s%s' % (username,times),now_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            coordinate.save()
        coordinateTimes = CoordinateTimes(times = coordinate,current_time = datetime.now(),longitude = longitude,latitude = latitude)
        coordinateTimes.save()
        return HttpResponse('success')
    
def get_map_src(objs):
    left = 180.0
    right = -180.0
    up = -90.0
    down = 90.0
    for obj in objs:
        if float(obj.longitude) > right:
            right = float(obj.longitude)
        if float(obj.longitude) < left:
            left = float(obj.longitude)
        if float(obj.latitude) > up:
            up = float(obj.latitude)
        if float(obj.latitude) < down:
            down = float(obj.latitude)
    left = left - 100
    right = right + 100
    up = up +100
    down = down -100
    if len(objs) == 1:
        return (1,objs[0].longitude,objs[0].latitude,objs[0].current_time)
    else:
        return (2,(left + (right-left)/2),(down+(up-down)/2),0)