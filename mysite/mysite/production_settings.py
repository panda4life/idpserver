PROD_SETTINGS = True
from settings import *
import os

DAEMON_IN_PATH = os.path.abspath('/home/idpserver/input')
DAEMON_OUT_PATH = os.path.abspath('/home/idpserver/output')

CAMPARI_PATH = os.path.abspath('/packages/campari/bin/x86_64/campari')
CAMPARI_KEYS = os.path.join(DAEMON_IN_PATH, '/campariKeys/')
HETERO_KEY = os.path.join(CAMPARI_KEYS, 'hetero.key')
WL_PATH = os.path.abspath('/packages/kappados/wl_main')

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pappulab.wustl.edu']

#HTTPS stuff
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
