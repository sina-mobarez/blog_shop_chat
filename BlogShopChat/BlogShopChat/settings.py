"""
Django settings for BlogShopChat project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y#sb+1h6zf4j4893kb=8b*4iy2#z8k#5-)0wbkx#a+hvmf6m95'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'accounts.apps.AccountsConfig',
    'blog',
    'shop',
    'webservice',
    #third party package for user registration and authentication endpoints 	
    'djoser',
    'django_filters',
	
    #rest API implementation library for django
    'rest_framework',
	
	#JWT authentication backend library
    'rest_framework_simplejwt',
    'crispy_forms',
    'widget_tweaks',
    'django_extensions',
    'channels',
    'chat.apps.ChatConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BlogShopChat.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

# WSGI_APPLICATION = 'BlogShopChat.wsgi.application'
ASGI_APPLICATION = 'BlogShopChat.asgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'finalproject', 
        'USER': 'postgres', 
        'PASSWORD': 'QWT67P53',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
ALLOWED_HOSTS=['*']

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# STATIC_ROOT = str(BASE_DIR /'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
BASE_DIR / 'static',
]

MEDIA_ROOT =  str(BASE_DIR /'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'landing-page'

# config/setting.py
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))
# sendgrid email host doesn't work
# we use gmail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mubarriizz@gmail.com'
EMAIL_HOST_PASSWORD = 'nlcoekbwswkpqocr'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

# LANGUAGE_CODE = 'fa-ir'    # for persian 

GRAPPELLI_ADMIN_TITLE = 'Final Project'
GRAPPELLI_CLEAN_INPUT_TYPES = True


# custom user 

AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']



'''

Endpoint	                     Description
--------------------------------------------------------------------------------------------------------------
/auth/users/	                 Register a new user
/auth/users/me/	                 retrieve/update the currently logged in user
/auth/jwt/create/	             create a JWT by passing a valid user in the post request to this endpoint
/auth/jwt/refresh/	             get a new JWT once the lifetime of the previously generated one expires
/api/accounts/all-profiles/	     get all user profiles and create a new one
/api/accounts/profile/id/	     detail view of a user's profile


'''

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}

