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
from . import facebook_blueprint


graphUrl = FbSettings.graphUrl
graphUrlId = FbSettings.graphUrlId
graphUrlPosts = FbSettings.graphUrlPosts
graphUrlVideos = FbSettings.graphUrlVideos


def typeMethodCity(method_name): #Datos agrupados por ciudad
	try:
		isValid = isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
			if validArgs["status"] == "error":
					return json.dumps(validArgs)
			if areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
				if areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = getToken(jsonData["account"])
					token = res_token["message"]
					url = buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"])
					req = requests.get(url)
					res = json.loads(req.text)
					jRes = [] #lista de datos que se muestran en json response
					for data in res["data"]:
						if data["period"] == "day":
							for values in data["values"]: 
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								claves = values["value"].keys()  #Ciudad, provincia, pais.
								lista_paises = [] 
								lista_provincias = []
								lista_ciudades = []
								for c in claves: #c es la clave
									valor_dato = values["value"][c] #valor de la clave 1, valor de la clave 2..
									clave_dato = c
									clave_dato_splitted = clave_dato.split(',')
									cantidad_divisiones = len(clave_dato_splitted)  
									if cantidad_divisiones > 3:
										ciudad = clave_dato_splitted[0]
										provincia = clave_dato_splitted[1]  #Provincia compuesta
										provincia = provincia.strip()
										for i in range(2, (len(clave_dato_splitted) - 1)):
											provincia = provincia + clave_dato_splitted[i]
										pais = clave_dato_splitted[3]
										pais = pais.strip()
										if pais not in lista_paises:
											lista_paises.append(pais)
										t_provincia = (provincia, pais) #prov, pais
										if t_provincia not in lista_provincias: 
											lista_provincias.append(t_provincia)

										t_ciudad = ((ciudad, valor_dato), provincia, pais)#ciudad y valor, provincia, pais
										if t_ciudad not in lista_ciudades:
											lista_ciudades.append(t_ciudad)

									if (cantidad_divisiones == 3):
										ciudad = clave_dato_splitted[0]
										provincia = clave_dato_splitted[1]
										provincia = provincia.strip()
										pais = clave_dato_splitted[2]
										pais = pais.strip()
										if pais not in lista_paises:
											lista_paises.append(pais)

										t_provincia = (provincia, pais) #prov, pais
										if t_provincia not in lista_provincias: 
											lista_provincias.append(t_provincia)

										t_ciudad = ((ciudad, valor_dato), provincia, pais)#ciudad y valor, provincia, pais
										if t_ciudad not in lista_ciudades:
											lista_ciudades.append(t_ciudad)
									else:
										if (cantidad_divisiones == 2):
											ciudad = clave_dato_splitted[0]
											pais = clave_dato_splitted[1]
											pais = pais.strip()
											if pais not in lista_paises:
												lista_paises.append(pais)

											t_ciudad = ((ciudad, valor_dato), None, pais)#ciudad y valor, nada, pais
											if t_ciudad not in lista_ciudades: 
												lista_ciudades.append(t_ciudad) 
								#Estructuro jerarquicamente localidad, con provincia , con pais.
								lista_pa = []
								for pais in lista_paises:
									lista_pr = []
									for provincia in lista_provincias:
										lista_ci = []
										for ciudad in lista_ciudades: #ciudades con provincia
											if ciudad[1] != None and ciudad[1] == provincia[0] and ciudad[2] == pais:
												lista_ci.append(ciudad[0])      
										if len(lista_ci) > 0:                               
											lista_pr.append((provincia[0], lista_ci))
									for ciudad in lista_ciudades: #ciudades sin provincia
										if ciudad[1] == None and ciudad[2] == pais:
											lista_pr.append((ciudad[0], None))
									lista_pa.append((pais, lista_pr))

								dic_pais = {}                        
								for pais in lista_pa:
									dic_provincia = {}
									for prov in pais[1]:#prov puede ser una ciudad y su valor, o una tupla (provincia,lista_ci)
										dic_ciudad = {}
										if prov[1] != None: #lista_ci
											for ciud in prov[1]: #itero en lista ciudades para esa prov
												dic_ciudad[ciud[0]] = ciud[1]
											dic_provincia[prov[0]] = dic_ciudad
										else:
											dic_provincia[prov[0][0]] = prov[0][1] 
									dic_pais[pais[0]] = dic_provincia 
								jRes.append(
								{
									fecha: dic_pais
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


@facebook_blueprint.route('/getPageFansCity', methods=['POST'])
def page_fans_city():
   return typeMethodCity("page_fans_city")


@facebook_blueprint.route('/getPageImpressionsByCityUnique', methods=['POST'])
def page_impressions_by_city_unique():
	return typeMethodCity("page_impressions_by_city_unique")