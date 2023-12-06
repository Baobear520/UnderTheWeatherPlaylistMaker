from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    'orca-app-qtor6.ondigitalocean.app',
    'orca-app-qtor6.ondigitalocean.app/undertheweatherplaylistmaker2',
    'localhost']

SECRET_KEY = os.environ.get('SECRET_KEY')


