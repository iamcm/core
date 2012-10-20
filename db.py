from pymongo import Connection
from application import settings

conn = Connection(settings.DBHOST, settings.DBPORT)

_DBCON = eval('conn.'+ settings.DBNAME)


