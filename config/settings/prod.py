from django.core.management.utils import get_random_secret_key
from .base import *


DEBUG = False

SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS')]