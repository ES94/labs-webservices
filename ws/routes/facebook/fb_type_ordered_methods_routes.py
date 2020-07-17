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
from flask import Flask, request, Blueprint

from . import facebook_blueprint
from .fb_settings import FbSettings
from classes.database import Database
from classes.settings import Settings
from classes.utils import Utils


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def typeMethodTypeOfOrdered(method_name): #Datos agrupados y ordenados por tipo de.. (reacciones, num. de veces, etc)
	try:
		isValid = Utils.isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
			if validArgs["status"] == "error":
					return json.dumps(validArgs)
			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = Utils.getToken(Settings.host, Settings.user, Settings.pswd, jsonData["account"])
					token = res_token["message"]
					url = Utils.buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"])
					req = requests.get(url)
					res = json.loads(req.text)
					jRes = [] #lista de datos que se muestran en json response
					for data in res["data"]:
						if data["period"] == "day":
							for values in data["values"]:                   
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								dic_info = {}
								claves = values["value"].keys()                       
								for c in claves: 
									valor_dato = values["value"][c] #valor de la clave 1, valor de la clave 2..
									clave_dato = c
									dic_info[clave_dato] = valor_dato
								dic_resultado = Utils.orderDictionary(dic_info)
								jRes.append({
									fecha: dic_resultado                                     
								})
					jsonResponse = Utils.getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)    
				else:
					return Utils.getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return Utils.getResponseJson("error", "Invalid data format or not data available")
	except:
		Utils.setLog()
		return Utils.getResponseJson("error", "Programming failure")


@facebook_blueprint.route('/getPageFansOnline', methods=['POST'])
def page_fans_online():
	return typeMethodTypeOfOrdered("page_fans_online")