"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import sys
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORS
    'corsheaders',

    # see https://www.django-rest-framework.org/
    'rest_framework',

    # 定时任务
    "django_apscheduler",

    # token
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    # 插入应用
    'bootstrap.apps.BootstrapConfig',
    'control.apps.ControlConfig',
    'scheduler.apps.SchedulerConfig',
    'file.apps.FileConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# 测试时使用sqlite3数据库（暂时不使用mysql数据库，有需要的可以取消注释）
# if 'test' in sys.argv or 'test_coverage' in sys.argv:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3'
#         }
#     }
# else:
#     DATABASES = {
#         # read os.environ['DATABASE_URL'] and raises
#         # ImproperlyConfigured exception if not found
#         #
#         # The db() method is an alias for db_url().
#         'default': env.db(),
#     }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
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

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 全局配置异常模块
    'EXCEPTION_HANDLER': 'bootstrap.exceptions.responst_exception_handler',
    # 修改默认返回JSON的renderer的类
    'DEFAULT_RENDERER_CLASSES': [
        'bootstrap.responses.ReponseRender'
    ],
    # 测试默认返回JSON格式
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'bootstrap.responses.ReponseRender'
    ]
}

# JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=123),  # 配置过期时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True
}

CORS_ORIGIN_WHITELIST = (
    'http://*',
    'https://*',
)

CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作。
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'Content-Type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

APSCHEDULER_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

# 腾讯云 COS 存储设置
COS_SECRED_ID = env('COS_SECRED_ID')
COS_SECRET_KEY = env('COS_SECRET_KEY')
COS_REDION = env('COS_REDION')
COS_BUCKET = env('COS_BUCKET')
# URL 生成的过期时间 单位：秒
COS_URL_EXPIRED = env('COS_URL_EXPIRED')
# COS 上存储的批量打包地址，请以斜杠结尾
COS_ARCHIVE_FULL_PATH = env('COS_ARCHIVE_FULL_PATH')

# Scrapy 打包文件地址
ARCHIVE_PATH = env('ARCHIVE_PATH')
# Scrapy 批量打包地址
ARCHIVE_FULL_PATH = env('ARCHIVE_FULL_PATH')
# Scrapy 打包文件名时间戳格式
ARCHIVE_DATETIME_FORMAT = env('ARCHIVE_DATETIME_FORMAT')
