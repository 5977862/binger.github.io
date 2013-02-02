#-*- coding:utf-8 -*-
# Django settings for mysite project.
import os

LOCATION_ENVIRONMENT = not os.environ.get('SERVER_SOFTWARE', False)

if LOCATION_ENVIRONMENT:
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Binger', 'tobinger@163.com'),
)

MANAGERS = ADMINS

if LOCATION_ENVIRONMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': r'sqlite.db',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '' ,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'app_relaxsae',                      # Or path to database file if using sqlite3.
            'USER': 'yy2330zxkw',                      # Not used with sqlite3.
            'PASSWORD': '1y3wkyl0j322yil2mwk1ylwim2llw1hi1mi1lz5w',                  # Not used with sqlite3.
            'HOST': 'w.rdc.sae.sina.com.cn' ,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': 3307,                      # Set to empty string for default. Not used with sqlite3.
        }
    }
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

STATIC_PATH = r''
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '**_yqx3hv1c8cvl7od6!m)8bc5os8n%@zlwsie%5zm1)od54j2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mysite.wsgi.application'

TEMPLATE_DIRS = (
                 "./template",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOGIN_URL = '/login'
#LOGOUT_URL = '/logout'

INSTALLED_APPS = (
    'news',
    'items',
    'userinfo',
    'message',
	'ifoundyou',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
#     'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MAIN_PAGE_PER_PAGE_LINES = 15
HOME_ITEM_LINES = 5
HOME_PER_LINE_LENGTH = 10

PROBLEM_PER_PAGE_LINES=15
RELAX_PER_PAGE_LINES=15
TUTSAU_PER_PAGE_LINES=15
HOME_ITEM_LINES=5
HOME_PER_LINE_LENGTH=10
WEB_SERVER_HOST='relaxsae.sinaapp.com'
ANDROID_CLIENT_VERSION='1.2',
NEW_USER_TITLE='欢迎来到这里'
NEW_USER_BODY='''感谢您的注册，
    
    在这里你可以文明地随意发言，发帖，如果有什么意见或建议，请与我私信，谢谢！'''
    
VAR_DICT={
    'PROBLEM_BTN_VALUE':'我要提问',
    'PROBLEM_TITLE_VALUE':'问题交流',
    'PROBLEM_BODY_VALUE':'在这里，你可以询问工作或生活上的疑问，也可以回答别人的问题，帮助他人，方便自己！',
    
    'RELAX_BTN_VALUE':'我要发起吃喝玩乐',
    'RELAX_TITLE_VALUE':'人生苦短，放松一下',
    'RELAX_BODY_VALUE':'日日夜夜的忙碌让人疲惫不堪，放松一下必不可少，你在等什么，快来加入吧，有好玩的好吃的记得带上别人哦！',
    
    'TUTSAU_BTN_VALUE':'有压力，我要说一说',
    'TUTSAU_TITLE_VALUE':'天天那么多烦心事，受不了啦',
    'TUTSAU_BODY_VALUE':'工作压力大，领导跟打了鸡血似的责备我，还要挣钱养家，我来说说我的苦',
    
    
    'PROBLEM_BTN_VALUE':'我要提问',
    'PROBLEM_TITLE_VALUE':'问题交流',
    'PROBLEM_BODY_VALUE':'在这里，你可以询问工作或生活上的疑问，也可以回答别人的问题，帮助他人，方便自己！',
    
    'RELAX_BTN_VALUE':'我要发起吃喝玩乐',
    'RELAX_TITLE_VALUE':'人生苦短，放松一下',
    'RELAX_BODY_VALUE':'日日夜夜的忙碌让人疲惫不堪，放松一下必不可少，你在等什么，快来加入吧，有好玩的好吃的记得带上别人哦！',
    
    'TUTSAU_BTN_VALUE':'有压力，我要说一说',
    'TUTSAU_TITLE_VALUE':'天天那么多烦心事，受不了啦',
    'TUTSAU_BODY_VALUE':'工作压力大，天天被责骂，有苦哪里说，不能老憋着，我来说说我的苦',
    
    'HOME_BTN_VALUE':'IfoundYou功能全新上线，赶快体验吧！',
    'HOME_TITLE_VALUE':'一个平凡的论坛',
    'HOME_BODY_VALUE':'一个平凡而简单的论坛，可以进行各种不一样的交流！(请使用非IE内核，建议使用Mozilla Firefox，Chrome内核)',
    'HOME_BTN_LINK':'/ifoundyou',
    
    'IFOUNDYOU_BTN_VALUE':'下载手机客户端(Android 2.1)',
    'IFOUNDYOU_TITLE_VALUE':'你在哪里，我找到你了',
    'IFOUNDYOU_BODY_VALUE':'IfoundYou是一项定位功能，使用GPS准确定位，通过分享自己的位置，使好友能够找到你！千里之外，我的好友，你在哪里，让我瞅瞅(⊙o⊙)',
    'IFOUNDYOU_BTN_LINK':'http://relaxsae-img.stor.sinaapp.com/img/IfoundYou.apk',
        
    'HOME_IMG_URL':'http://relaxsae-img.stor.sinaapp.com/img/home.jpg',
    'PROBLEM_IMG_URL':'http://relaxsae-img.stor.sinaapp.com/img/problem.png',
    'RELAX_IMG_URL':'http://relaxsae-img.stor.sinaapp.com/img/relax.png',
    'IFOUNDYOU_IMG_URL':'http://relaxsae-img.stor.sinaapp.com/img/map.png',
    'TUTSAU_IMG_URL':'http://relaxsae-img.stor.sinaapp.com/img/tutsau.png'
}

FORUM_LIST=['problem','relax','tutsau']