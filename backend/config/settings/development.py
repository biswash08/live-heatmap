from .base import *

DEBUG = True

DATABASES['default']['HOST'] = env('POSTGRES_HOST', default='localhost')
DATABASES['default']['PORT'] = env('POSTGRES_PORT', default='5432')
