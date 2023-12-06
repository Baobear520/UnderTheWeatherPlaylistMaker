from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'orca-app-qtor6.ondigitalocean.app','localhost']

SECRET_KEY = os.environ.get('SECRET_KEY')


