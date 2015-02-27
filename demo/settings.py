"""
Django settings for demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""


import os
import logging


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')f)l0#v2ib#=#$40j)kog@e6b@2dzj(4oz*rzc#f)u88^t*)ng'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'demo/templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_auth_qr2auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django_auth_qr2auth.backend.QR2AuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'django.contrib.auth.views.login'
LOGOUT_URL = 'django.contrib.auth.views.logout'
LOGIN_REDIRECT_URL = '/qrtoauth/'


# QRtoAuth passphrase to decrypt the user shared_secrets
Q2A_PASSPHRASE = 'V/SfuEUwBVg4XI8Csbs8hZDoV4QNmaPbRQfvnU+/KqpiHHJmbmqHtDWbxH51Ok95'
# Q2A_OTP_LENGTH must be in range(6, 10)
Q2A_OTP_LENGTH = 6
# Revoke QR2Auth shared secret after 5 failed authentication attempts
Q2A_MAX_AUTH_TRIES = 5


# setup logging
logging.basicConfig(level = logging.INFO,
                    format = '%(asctime)s %(levelname)s %(message)s',
                    )

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(
        os.path.dirname(__file__),
        'static',
    ),
)
