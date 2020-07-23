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

import MySQLdb
from waitress import serve
from flask import Flask, request
from werkzeug import serving, wrappers


from classes.database import Database
from classes.settings import Settings
from classes.utils import Utils
from chatbots import chatbots_blueprint
from chatbots.facebook import facebook_blueprint
from chatbots.instagram import instagram_blueprint
from chatbots.web import web_blueprint
from chatbots.whatsapp import whatsapp_blueprint


__appHostname = '0.0.0.0'
__appPort = 5001
app = Flask(__name__)

app.register_blueprint(chatbots_blueprint, url_prefix='/chatbots')
app.register_blueprint(facebook_blueprint, url_prefix='/chatbots/fb')
app.register_blueprint(instagram_blueprint, url_prefix='/chatbots/ig')
app.register_blueprint(web_blueprint, url_prefix='/chatbots/wb')
app.register_blueprint(whatsapp_blueprint, url_prefix='/chatbots/wa')


if __name__ == '__main__':
	try:
		reload(sys)

		# EN PRODUCCION, CON LOS CERTIFICADOS CORRESPONDIENTES
        # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context.load_cert_chain(__sslCert, __sslKey)
        # serving.run_simple(__appHostname, __appPort, app, threaded=True, ssl_context=context)

		# DESARROLLO
		serving.run_simple(__appHostname, __appPort, app)
	except:
		Utils.setLog()
