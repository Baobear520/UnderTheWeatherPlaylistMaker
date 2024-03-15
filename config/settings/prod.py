from django.core.management.utils import get_random_secret_key
from .base import *


DEBUG = False

SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS')]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
} 

CELERY_BROKER_URL = "redis://redis:6379/2"
CELERY_RESULT_BACKEND = "redis://redis:6379/3"