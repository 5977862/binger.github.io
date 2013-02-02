from django.conf.urls import patterns, include, url
from views import login_action,home_action,submit_words_action,change_password_action,checkuser_action
from news.views import news_action,news_single_action
from catchnews.views import catch_news_action
from items.views import add_item_action,item_action,single_item_action,item_new_action,join_action,joined_action
from userinfo.views import activity_action,edit_user_action,userinfo_submit_action,userinfo_action,forget_passwd_action,getpasswd_action,regiest_action,success_action,error_action
from ifoundyou.views import getcoordinate_action,ifoundyou_action,ifoundyou_by_phone,ifoundyou_by_time,ifoundyou_set_permission_action
from message.views import single_message_action,message_action,delete_message_action,new_message_action

from django.contrib.auth.views import logout
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':'./static/css' }),
    (r'^img/(?P<path>.*)$','django.views.static.serve',{'document_root':'./static/img' }),
    (r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root':'./static/js' }),
    (r'^admin',include(admin.site.urls)),
    (r'^(news)/(\d{1,3}$)',news_single_action),
    (r'^(news)$',news_action),
    
    (r'^forum/new_(\w*)$',item_new_action),
    (r'^forum/add_(\w*)$',add_item_action),
    (r'^forum/single_(\w*)$',single_item_action),
    (r'^forum/(\w*)$',item_action),
    
    (r'^join$',join_action),
    (r'^joined$',joined_action),
    
    (r'^submitwords$',submit_words_action),
    (r'^regiest$',regiest_action),
    (r'^login$',login_action),
    (r'^logout$',logout),
    (r'^checkuser$',checkuser_action),
    
    (r'^catchnews$',catch_news_action),
    (r'^userinfo$',userinfo_action),
    (r'^forgetpasswd$',forget_passwd_action),
    (r'^getpasswd$',getpasswd_action),
    (r'^submit_user$',userinfo_submit_action),
    (r'^activity$',activity_action),
    (r'^edit$',edit_user_action),
    (r'^change_passwd$',change_password_action),
    
    (r'^message$',message_action),
    (r'^message/(\d{1,3})$',single_message_action),
    (r'^del_message/(\d{1,3})$',delete_message_action),
    (r'^new_message/(\w*)$',new_message_action),
    
    (r'^getcoordinate$',getcoordinate_action),
    (r'^(ifoundyou)$',ifoundyou_action),
    (r'^(ifoundyou)byphone$',ifoundyou_by_phone),
    (r'^(ifoundyou)bytime$',ifoundyou_by_time),
    (r'^ifoundyou_set_permission$',ifoundyou_set_permission_action),
    
    (r'^success$',success_action),
    (r'^error$',error_action),
    
    (r'[/s/S]*',home_action),
    
)
