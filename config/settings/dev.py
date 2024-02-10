from .base import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', os.environ.get('DJANGO_ALLOWED_HOSTS')]

SECRET_KEY = '_!acfcjalq49#s#y4o*92se1mv=yumpsmzcdnbd^sx$l_s8ko6'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
} 