"""
Django settings for sk8_bot project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_TYPE = env("SITE_ADDRESS")
ENV_TYPE = env("ENV_TYPE")
if ENV_TYPE == "dev":
    ALLOWED_HOSTS = ["*"]
elif ENV_TYPE == "prod":
    SECURE_SSL_REDIRECT = True
    # ALLOWED_HOSTS = [SITE_ADDRESS] add slack and telegram?
    ALLOWED_HOSTS = ["*"]  # See if i can get rid of this later


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = env("SECRET_KEY")

DEBUG = True if ENV_TYPE == "dev" else False
SECURE_SSL_REDIRECT = True if ENV_TYPE == "prod" else False


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS += ["webhooks_consumer"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sk8_bot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "sk8_bot.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"

ADMINS = [("Mic", env("ADMIN_EMAIL"))]

# to use: python manage.py createcachetable
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'webhooks_consumer',
    }
}

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
# do i really use these in testing or can i get rid of?
TELEGRAM_APP_API_ID = env("TELEGRAM_APP_API_ID")
TELEGRAM_APP_API_HASH = env("TELEGRAM_APP_API_HASH")
TELETHON_SESSION = env("TELETHON_SESSION")
SLACK_BOT_TOKEN = env("SLACK_BOT_TOKEN")
