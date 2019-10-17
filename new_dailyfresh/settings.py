"""
Django settings for new_dailyfresh project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# 加这行
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加上这行代码可以直接写app名，不用apps.app名
sys.path.insert(0, os.path.join(BASE_DIR,'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5+rgd-+5_@c!rsxswg=bnd_69v+nddzf^@6$6)c*o91tx=_i8^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'user',
    'goods',
    'order',
    'cart',
    'haystack' # 全文检索框架
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'new_dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'new_dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh_lyc1',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '192.168.31.131',
        'PORT': 3306 ,
    }
}
# django认证系统使用我们这个模型类（user应用下的User类）
# 必须指定，要不然迁移生成表会报错，目的是替换django默认生成的认证模型类（auth_user表）
AUTH_USER_MODEL = 'user.User'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

# 富文本编辑器的配置
TINYMCE_DEFAULT_CONFIG = {
    'theme':'advanced',
    'width':600,
    'height':400,
}

# 发送邮件设置 163邮箱
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 固定写法
EMAIL_HOST = 'smtp.163.com' # SMTP地址
EMAIL_PORT = 25 # SMTP端口
EMAIL_HOST_USER = 'lanyuechun592@163.com' #发送邮件的邮箱
EMAIL_HOST_PASSWORD = 'asd758520lyc'  # 授权码，163邮箱中设置的
# 发件人，<>里面的东西必须和EMAIL_HOST_USER（目的邮箱地址一摸一样，不能随便写，不然邮件发不出去）
EMAIL_FROM = '天天生鲜<lanyuechun592@163.com>'

# django的缓存配置
CACHES = {
    'default':{
        'BACKEND': 'django_redis.cache.RedisCache',
        # 将用户的session信息存储在ubuntu上的redis的9号数据库里
        'LOCATION': 'redis://192.168.31.131:6379/9',
        'OPTIONS':{
            'CLIENT+CLASS':'django_redis.client.DefaultClient',
        }
    }
}

# 存储sesiion的配置
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# 配置login_required函数如果检测到用户没有登录，是不能访问/user,/user/order,/user/adress的，但是django框架用户认证系统的这个函数默认跳转的url地址是/accounts/login/?next=/user/，我们应该把这个函数的跳转地址改为登陆页面。
LOGIN_URL='/user/login'



# <修改django的上传行为>
# 设置Django的文件存储类，我把它指定出来，并在我们的指定类中连接我的fastdfs服务器 来存储文件，不用django自带的文件存储系统了
DEFAULT_FILE_STORAGE='utils.fdfs.storage.FDFSStorage'

# 这两个可以随意（要有意义）起名字，只是我们传的参数，但是像上面的是我们修改的django框架里面默认项，只能用原变量名
# 设置fastdfs储存服务器使用的客户端配置文件
FDFS_CLIENT_CONF = './utils/fdfs/client.conf'

# 设置fastdfs存储服务器上的nginx服务器的ip及端口,定义这个之后，以后我们要在前段显示一张图片
# 只需在django(改变上传行为)后台上传,这个上传就是指上传到了fastdfs了,然后你在前段显示一张上传好的图片只需.url即可，nginx马上给你返回
FDFS_URL='http://192.168.31.131:8888/'


# 全文检索框架的配置
HAYSTACK_CONNECTIONS = {
    'default': {
        #使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',    # 其实这就是whoosh引擎的路径
        #索引文件路径 存放索引目录
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
#当表中发生添加、修改、删除数据时，自动生成索引，即生成分词，等着搜索框匹配
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 指定搜索结果中每一页显示多少个结果，等于１就是每页只显示一个搜索结果
HAYSTACK_SEARCH_RESULTS_PER_PAGE=1