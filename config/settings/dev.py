from .base import *


DEBUG = True

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS'),'localhost','127.0.0.1','0.0.0.0']

SECRET_KEY = '_!acfcjalq49#s#y4o*92se1mv=yumpsmzcdnbd^sx$l_s8ko6'

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

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# } 

# CELERY_BROKER_URL = "redis://127.0.0.1:6379/2"
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/3"