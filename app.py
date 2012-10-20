import os 
import sys


if len(sys.argv)==1: 
	raise ValueError('No application rootpath defined')
else:
	_ROOTPATH = sys.argv[1]

# add this application to the python path
sys.path.append(_ROOTPATH)

from beaker.middleware import SessionMiddleware
from core import bottle
from application import settings
# override the template path if we have had one specified BEFORE importing the routes
try:
	bottle.TEMPLATE_PATH = settings.TEMPLATE_PATH
except:
	pass
# now import the routes
from core.routes import *
from application.routes import *

session_opts = {
	'session.auto':True,
	'session.cookie_expires': 60 * 60 * 60,
	'session.key':'se',	
	'session.type':'file',
	'session.data_dir':'/home/chris/code/_beaker_sessions',
}

app = SessionMiddleware(bottle.app(), session_opts)

if __name__ == '__main__':
    with open(settings.ROOTPATH +'/app.pid','w') as f:
        f.write(str(os.getpid()))

    if settings.DEBUG: 
        bottle.debug() 
        
    bottle.run(app=app, server=settings.SERVER, reloader=settings.DEBUG, host=settings.APPHOST, port=settings.APPPORT, quiet=(settings.DEBUG==False) )
    