"""
Django settings for alexandria_server project.

Generated by 'django-admin startproject' using Django 1.10.
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get('DEBUG'):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # Core
    'django.contrib.contenttypes',
    'django.contrib.messages',
    # Third-party
    'rest_framework',
    # Internal
    'alexandria_server.permissions',
    'alexandria_server.projects',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alexandria_server.urls'

WSGI_APPLICATION = 'alexandria_server.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'UNAUTHENTICATED_USER': None
}

# GitHub settings
GITHUB_OAUTH_URL = "https://github.com/login/oauth/"
GITHUB_API_URL = "https://api.github.com/"

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
