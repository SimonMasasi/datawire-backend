"""
Django settings for datawire project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9zoa=kfdpy6u4+!1)vq^_ejh+^3b#ury6&e!($9&d@ld&96pw6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'monitor',
    'rest_framework',
    'rest_framework.authtoken',
    'location_field.apps.DefaultConfig',
    'corsheaders',
    'datasetApp',
    'authApp',
    'modelAPP',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datawire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'datawire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

MAX_UPLOAD_SIZE = 214958080
DATA_UPLOAD_MAX_MEMORY_SIZE=214958080
DATA_UPLOAD_MAX_NUMBER_FILES=1000000
FILE_UPLOAD_MAX_MEMORY_SIZE=214958080



NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
]

try:
    import jupyterlab
    NOTEBOOK_DEFAULT_URL = '/lab'  # Using JupyterLab
except ImportError:
    NOTEBOOK_DEFAULT_URL = '/tree'  # Using Jupyter

NOTEBOOK_DIR = BASE_DIR / "notebooks"

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    '--notebook-dir', NOTEBOOK_DIR,
    '--NotebookApp.default_url', NOTEBOOK_DEFAULT_URL,
]
IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'

IPYTHON_KERNEL_DISPLAY_NAME = 'Django Kernel'

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
    #    'rest_framework.authentication.SessionAuthentication',
       'rest_framework.authentication.TokenAuthentication',
    #    'authApp.auth_backend.CustomAuthTokenBackend',
   )
}

CORS_ALLOWED_ORIGINS = [
   "http://localhost:4000",
   "http://127.0.0.1:4000",
   "http://172.17.17.159:4000",
    "http://localhost:4000",
    "http://127.0.0.1:4200",
    "http://localhost:4200",
    "http://localhost:4000",
    "https://data-set-repository.netlify.app",
]

# DEFAULT_RENDERER_CLASSES = (
#     'rest_framework.renderers.JSONRenderer',
#     # ... other renderers if needed
# )

# DEFAULT_PARSER_CLASSES = (
#     'rest_framework.parsers.JSONParser',
#     # ... other parsers if needed
# )

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

#api for browsing map

LOCATION_FIELD = {
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': '<PLACE YOUR API KEY HERE>',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

AUTH_USER_MODEL="authApp.CustomUser"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587  # Typically 587 for TLS, 465 for SSL
EMAIL_HOST_USER = 'tensonmtawa@yahoo.com'
EMAIL_HOST_PASSWORD = 'bwgshfikgigvbcyo'
EMAIL_USE_TLS = True  # Use TLS for secure communication
# Optionally, for development/testing:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'