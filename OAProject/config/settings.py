"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os.path
from pathlib import Path

# __file__引用当前 settings.py 文件
# .resolve()返回绝对路径
# .parent.parent上升两个级别 - 到项目目录
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!， 用于加密签名的随机生成的字符串
SECRET_KEY = 'django-insecure-jlcgo6-f-nv)1#*m*3dp_vqu+e^%)wiyv-#z1+yr0r*^)(-h(#'

# DEBUG = True用于开发环境，DEBUG = False用于生产环境
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# 告诉Django所用到的应用程序
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 为静态文件提供服务
    'django.contrib.staticfiles',
    # 将应用程序OAUser的配置告诉django
    'OAUser.apps.OauserConfig',
    # captcha（验证码）对于需要用户注册、依赖用户生成内容的Web 应用程序，防止自动机器人向 Web 表单发送垃圾邮件，验证码功能
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全相关的中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 处理会话的中间件
    'django.middleware.common.CommonMiddleware',  # 处理跨站点请求的中间件
    'django.middleware.csrf.CsrfViewMiddleware',  # 处理CSRF的中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 身份验证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 处理消息的中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护
]

# Django 将使用 config/urls.py 文件作为应用程序的 URL 路由配置模块。
ROOT_URLCONF = 'config.urls'

# Django 自带的模板引擎，并启用了应用程序模板目录（APP_DIRS=True），django将在每个app的templates目录下找模板文件
# 'DIRS': [os.path.join(BASE_DIR), 'templates']设置templates目录在项目根目录下
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'templates']
        ,
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

# Django 将使用config/wsgi.py 文件中的 application 对象作为 WSGI 应用程序的入口点
WSGI_APPLICATION = 'config.wsgi.application'

# 所使用的数据库
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# OPTIONS是一个可选字典，用于指定特定数据库引擎的选项
# 将autocommit设置为True时，每个数据库操作会自动提交到数据库中，立即生效，形成一个新的事务。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'account',
        'USER': 'gbz',  # 自己的db账户名
        'PASSWORD': 'guobenzheng8888',  # 自己的db账户密码
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'  # 语言

TIME_ZONE = 'Asia/Beijing'  # 时区

USE_I18N = True

USE_L10N = True

USE_TZ = False

# 静态文件(CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_ROOT：静态文件在（生产环境）中的存储位置
# 静态文件在web的 URL（开发环境）将以 `/static/` 开头
STATIC_URL = '/static/'
# 设置静态文件目录，BASE_DIR 表示项目的根目录。os.path.join() 函数用于将根目录与../static拼接,
# 一个点表示static位于当前目录中，两个点表示static目录位于当前目录的父目录中
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../static'),
]

# 搜索应用程序目录中的静态文件。
STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 设置models中使用的主键自增字段的类型为BigAutoField
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
