import os
import environ

# import dj_database_url
import django_heroku
from pathlib import Path
from datetime import timedelta

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("ENVIRONMENT") == "DEVELOPMENT"

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "drf_yasg",
    "rest_framework",
    "channels",
    "corsheaders",
    # local
    "authentication",
    "rental",
    "user",
    "review",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "base.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "base.wsgi.application"

# Local Database
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Remote Database
# Using a Database URL
# DATABASES = {
#     "default": dj_database_url.config(default=env("DATABASE_URL"), conn_max_age=600)
# }

DATABASES = {
    "default": {
        "ENGINE": env("DATABASE_ENGINE"),
        "HOST": env("DATABASE_HOST"),
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "PORT": env("DATABASE_PORT"),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

django_heroku.settings(locals())

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SIGNING_KEY": env("JWT_SECRET_KEY"),
    "ALGORITHM": env("JWT_ALGORITHM"),
}

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = ["https://marketyapi.up.railway.app"]

# Documentation
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Auth Token eg [Bearer JWT]": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    }
}

# Daphne
ASGI_APPLICATION = "base.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    }
}
