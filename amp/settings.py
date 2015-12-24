"""
Django settings for amp project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

STATIC_PATH = os.path.join(BASE_DIR,'static')

# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     TEMPLATE_PATH,
# )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'st(h2bn3-c5&$)81c!xta)e&jk%c8&arepo)0tv&6aeix$vyon'

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
    'app',
    'social_auth',
    'storages',
    'bootstrapform',
    'widget_tweaks',
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


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'app.pipeline.create_user_profile',
)


ROOT_URLCONF = 'amp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
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

WSGI_APPLICATION = 'amp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hta',
        'USER': 'karanhta',
        'PASSWORD': 'karanhta123',
        'HOST': 'karanhta.ceimievu2nzy.us-west-2.rds.amazonaws.com',
        'PORT': '3306'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGIN_ERROR_URL = '/error/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/user/home/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/user/phone/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

# SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email','phone']
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'pl_PL',
  'fields': 'id, name, email',
}
FACEBOOK_APP_ID = '1038816236180427'
FACEBOOK_API_SECRET = '9ab6f56c299b3f3485711b4a8443f72a'
GOOGLE_OAUTH2_CLIENT_ID = '420023432978-9qj38ci17j24vonlujh4nmum5r3fabmt.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'stxYBnvRvBwYHDnBNEZZegp7'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'mnik@hghm.com'
# EMAIL_HOST_PASSWORD = 'yourpasshere'
# DEFAULT_FROM_EMAIL = 'mkinsrfd.com'
# DEFAULT_TO_EMAIL = 'monik@etiole.com'

AWS_STORAGE_BUCKET_NAME = 'imgmed'
AWS_ACCESS_KEY_ID = 'AKIAJ2DCUNJYTKUQZ5UQ'
AWS_SECRET_ACCESS_KEY = 'PkX9I2Tr7A+8kIKE+mN1PQK+E5GXkFiWZk/kFAfr'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'amp.custom_storage.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)


MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'amp.custom_storage.MediaStorage'

try:
    from settings_local import *
except ImportError:
    pass