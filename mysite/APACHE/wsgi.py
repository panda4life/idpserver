# wsgi.py
import os, sys
sys.path.append('/home/idpserver/idpserver') #parent directory of project
sys.path.append('/home/idpserver/idpserver/mysite')
#You might not need this next line. But if you do, this directory needs to be world-writable.
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi

#HTTPS Stuff
#os.environ['HTTPS'] = "on"
#os.environ['wsgi.url_scheme'] = 'https'

_application = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    environ['SCRIPT_NAME'] = '' # my little addition to make it work
    return _application(environ, start_response)