"""
Django settings for message_board project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lp9+h)@+^vp4*9cvyyeyhfx)amiibjp%ujjvm&)9^mrzrlx)v4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
env = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_filters',
    #app
    'models',

    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #https://github.com/django-ckeditor/django-ckeditor
    'ckeditor',
    'ckeditor_uploader',
    
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #allauth middleware
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'message_board.urls'

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
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'message_board.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


#allauth backends

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    ]

#allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {"signup": "models.forms.CustomSignupForm"}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
PROJECT_DIR=os.path.dirname(__file__)

#STATIC_ROOT = [BASE_DIR / 'static_media/'] don't work
#static
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT= os.path.join(PROJECT_DIR,'static_media/')
STATIC_URL = 'static/'

#media
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media/')
MEDIA_URL = 'media/'
#auth

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/board/'

LOGOUT_REDIRECT_URL = '/account/login/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#ckeditor
from ckeditor.configs import DEFAULT_CONFIG  # noqa
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default':DEFAULT_CONFIG,
    'awesome_ckeditor': {
    "skin": "moono-lisa",
    "toolbar_Basic": [["Source", "-", "Bold", "Italic"]],
    "toolbar_Full": [
        [
            "Styles",
            "Format",
            "Bold",
            "Italic",
            "Underline",
            "Strike",
            "SpellChecker",
            "Undo",
            "Redo",
        ],
        ["Link", "Unlink", "Anchor"],
        ["Image", "Html5video", "Flash", "Table", "HorizontalRule"],
        ["TextColor", "BGColor"],
        ["Smiley", "SpecialChar"],
        ["Sourcedialog", ],
    ],
    "toolbar": "Full",
    "height": 291,
    "width": "100%",
    "filebrowserWindowWidth": 940,
    "filebrowserWindowHeight": 725,
    'extra_plugins':['html5video', 'sourcedialog',],
    'external_plugin_resources':[(
        'html5video',
        '/static/plugins/ckeditor-html5-video-master/html5video/',
        'plugin.js',
        ),
            ],
    "removePlugins": ['sourcearea', 'iframe'],
    'extraAllowedContent' : ['iframe[*]'],

    

    }
}
#email settings

if DEBUG and not env:

    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = "example@yandex.ru"
    EMAIL_HOST_PASSWORD = "iliezvcovrxqizez"
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = "example@yandex.ru"
    EMAIL_SUBJECT_PREFIX = "TEST"
    
else:
    load_dotenv()
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = 'smtp.yandex.ru'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = True
    DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
    SERVER_EMAIL = os.getenv('EMAIL_HOST_USER')
    EMAIL_SUBJECT_PREFIX = '[TEST]',
    ADMINS = list(os.getenv('ADMINS'))
