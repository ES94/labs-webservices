import os
import inspect
import traceback
import sys
import requests
import simplejson as json
import calendar
import time
import collections
import hashlib
from time import gmtime, strftime
from datetime import date, datetime
from importlib import reload

import MySQLdb as db
from waitress import serve
from flask import Flask, request
from werkzeug.serving import run_simple

from classes.database import Database
from classes.utils import Utils
from routes.facebook import facebook_blueprint
from routes.instagram import instagram_blueprint
from routes.whatsapp import whatsapp_blueprint


__appHostname = '0.0.0.0'
__appPort = 5001
app = Flask(__name__)

app.register_blueprint(facebook_blueprint, url_prefix='/facebook')
app.register_blueprint(instagram_blueprint, url_prefix='/instagram')
app.register_blueprint(whatsapp_blueprint, url_prefix='/whatsapp')


if __name__ == '__main__':
	try:
		reload(sys)

		# EN PRODUCCION, CON LOS CERTIFICADOS CORRESPONDIENTES
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context.load_cert_chain(__sslCert, __sslKey)
        # serving.run_simple(__appHostname, __appPort, app, threaded=True, ssl_context=context)

		# DESARROLLO
		run_simple(__appHostname, __appPort, app)
	except:
		Utils.setLog()
