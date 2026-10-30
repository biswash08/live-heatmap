from .base import *

DEBUG = False

DATABASES['default']['HOST'] = env('POSTGRES_HOST', default='postgres')
DATABASES['default']['PORT'] = env('POSTGRES_PORT', default='5432')
