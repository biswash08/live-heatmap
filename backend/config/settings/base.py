import os
from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY', default='insecure-development-secret-key')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

GDAL_LIBRARY_PATH = env('GDAL_LIBRARY_PATH', default=None)
USE_GIS = env('USE_GIS', default='false').lower() == 'true' or bool(GDAL_LIBRARY_PATH)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'daphne',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'channels',
    'corsheaders',
    'apps.authentication',
    'apps.drivers',
    'apps.locations',
    'apps.geospatial',
    'apps.heatmap',
    'apps.driver_search',
    'apps.surge_pricing',
    'apps.rides',
    'apps.cities',
    'apps.analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

if USE_GIS:
    INSTALLED_APPS.insert(6, 'django.contrib.gis')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis' if USE_GIS else 'django.db.backends.sqlite3',
        'NAME': env('POSTGRES_DB', default=str(BASE_DIR / 'db.sqlite3')) if USE_GIS else str(BASE_DIR / 'db.sqlite3'),
        'USER': env('POSTGRES_USER', default='postgres') if USE_GIS else '',
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres') if USE_GIS else '',
        'HOST': env('POSTGRES_HOST', default='localhost') if USE_GIS else '',
        'PORT': env('POSTGRES_PORT', default='5432') if USE_GIS else '',
    }
}

REDIS_URL = env('REDIS_URL', default='redis://127.0.0.1:6379/0')
KAFKA_BOOTSTRAP_SERVERS = env('KAFKA_BOOTSTRAP_SERVERS', default='localhost:9092')
KAFKA_TOPIC_DRIVER_LOCATION = env('KAFKA_TOPIC_DRIVER_LOCATION', default='driver-location-events')
KAFKA_DLQ_TOPIC = env('KAFKA_DLQ_TOPIC', default='driver-location-events-dlq')
KAFKA_CONSUMER_GROUP = env('KAFKA_CONSUMER_GROUP', default='location-processor-v1')

USE_REDIS_CHANNELS = env('USE_REDIS_CHANNELS', default='false').lower() == 'true'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer' if not USE_REDIS_CHANNELS else 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [env('CHANNEL_LAYERS_URL', default=REDIS_URL)],
        },
    }
} if USE_REDIS_CHANNELS else {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Real-Time Driver Heatmap API',
    'DESCRIPTION': 'Real-time driver tracking, heatmap, surge pricing and nearby driver APIs.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

H3_RESOLUTION = int(env('H3_RESOLUTION', default='8'))
DRIVER_LOCATION_TTL_SECONDS = int(env('DRIVER_LOCATION_TTL_SECONDS', default='30'))
