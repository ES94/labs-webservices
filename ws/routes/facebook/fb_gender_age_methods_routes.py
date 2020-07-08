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

from .fb_settings import FbSettings
from classes.database import Database
from classes.utils import Utils
from facebook import facebook_blueprint


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def typeMethodGenderAge(method_name): #Datos agrupados por genero en rango de edades.
	try:
		isValid = isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = areValidPostArguments(jsonData, ["account" , "date_since", "date_until"])
			if validArgs["status"] == "error":
				return json.dumps(validArgs)
			if areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):#Chequeo fechas UNIX validas
				if areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = getToken(jsonData["account"])
					token = res_token["message"]
					url = buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"]) 
					req = requests.get(url)
					res = json.loads(req.text)           
					jRes = []
					for data in res["data"]:
						if data["period"] == "day":
							for values in data["values"]:                   
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								dic_male = {}
								dic_female = {}
								dic_undefined = {}
								claves = values["value"].keys()                       
								for c in claves: #c es la clave
									valor_dato = values["value"][c] #valor de la clave 1, valor de la clave 2..
									clave_dato = c
									clave_dato_splitted = clave_dato.split('.')                        
									clave_genero = clave_dato_splitted[0] #Genero
									clave_info = clave_dato_splitted[1] #Info del genero
									#DATOS A MOSTRAR clave_genero, clave_info, valor_dato
									if (clave_genero == 'M'):
										dic_male[clave_info] = valor_dato
									if (clave_genero == 'F'):
										dic_female[clave_info] = valor_dato
									if (clave_genero == 'U'):
										dic_undefined[clave_info] = valor_dato
								jRes.append({
									fecha: {
										"female": dic_female,
										"male": dic_male,
										"undefined": dic_undefined
									}
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


@facebook_blueprint.route('/getPageContentActivityByAgeGenderUnique', methods=['POST'])
def page_content_activity_by_age_gender_unique():
	return typeMethodGenderAge("page_content_activity_by_age_gender_unique") 


@facebook_blueprint.route('/getPageImpressionsByAgeGenderUnique', methods=['POST'])
def page_impressions_by_age_gender_unique():
	return typeMethodGenderAge("page_impressions_by_age_gender_unique")


@facebook_blueprint.route('/getPageFansGenderAge', methods=['POST'])
def page_fans_gender_age():
	return typeMethodGenderAge("page_fans_gender_age")