import os
import inspect
import traceback
import sys
import requests
import simplejson as json
import calendar
import time
import collections
import MySQLdb as db
from classes.database import Database
from waitress import serve
from flask import Flask
from flask import request
import hashlib
from datetime import date, datetime
from time import gmtime, strftime

host = "127.0.0.1"
user = "root"
pswd = ""

graphUrl = "https://graph.facebook.com/v4.0/me/insights?"
graphUrlPosts = "https://graph.facebook.com/v4.0/me/posts?"
#graphUrlVideos = "https://graph.facebook.com/v4.0/me/videos?"
graphUrlId = "https://graph.facebook.com/v4.0/me?"

app = Flask(__name__)

def getPageId(token):
	url = graphUrlId + "access_token=" + token 
	req = requests.get(url)
	res = json.loads(req.text)
	name = res["name"]
	pageId = res["id"]
	return pageId


def setLog():
	try:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		error = repr(traceback.format_exception("", exc_value, exc_traceback))
		origin = inspect.stack()[1][3]
		now = datetime.now()
		time = now.strftime("%d/%m/%Y %H:%M:%S")
		stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
		with open(r"D:\eniac\LABS357 Dashboard\Webservices LABS\ws\logs\metrics.log", "a") as logFile:
			logFile.write(stringError)
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		error = repr(traceback.format_exception("", exc_value, exc_traceback))
		origin = inspect.stack()[1][3]  
		now = datetime.now()
		time = now.strftime("%d/%m/%Y %H:%M:%S")
		stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
		with open(r"D:\eniac\LABS357 Dashboard\Webservices LABS\ws\logs\metrics.log", "a") as logFile:
			logFile.write(stringError)

def buildUrl(baseUrl, token, metric, date_since, date_until):
	return baseUrl + "access_token=" + token + "&metric=" + metric + "&since=" + str(date_since) + "&until=" + str(date_until)

def buildUrlPost(pageId, postId, token, metric, date_since, date_until):
	return "https://graph.facebook.com/v4.0/" + pageId + "_" + postId + "/insights?" + "access_token=" + token + "&metric=" + metric + "&since=" + str(date_since) + "&until=" + str(date_until)

def computeMD5hash(my_string):
	m = hashlib.md5()
	m.update(my_string.encode('utf-8'))
	return m.hexdigest()

def getToken(account):
	DATABASE = Database.getInstance(host,user,pswd,"plataforma")
	query = "SELECT I.password FROM instancias I"
	query = query + " WHERE I.id_medio = 2"
	query = query + " and I.id_cuenta =" + str(account)
		   
	res = DATABASE.executeQuery(query, None, True)
	if res is not None and len(res) == 1: #Deberia haber solo una cuenta con ese ID
		token = res[0][0]
		return getResponseJson("success", token, False) 
	else:
		if res is None:
			return getResponseJson("error", "Account not found", False)
		else:
			return getResponseJson("error", "There are many accounts with that id", False)

def isValidJsonData(request):
	if request.data:
		if request.is_json:
			try:
				jsonData = json.loads(request.data)
				return True
			except:
				return False
		else:
			return False
	else:
		return False
	
def areValidPostArguments(jsonData, args):
	invalidArgs = []
	for a in args:
		if a not in jsonData:
			invalidArgs.append(a)

	if (len(invalidArgs) > 0):
		return getResponseJson("error", "The following arguments are required: " + ", ".join(invalidArgs), False)
	else:
		return getResponseJson("success", "Ok", False)
	
def areValidGetArguments(request, args):
	invalidArgs = []
	for a in args:
		if request.args.get(a) is None:
			invalidArgs.append(a)

	if (len(invalidArgs) > 0):
		return getResponseJson("error", "The following arguments are required: " + ", ".join(invalidArgs), False)
	else:
		return getResponseJson("success", "Ok", False)

def getResponseJson(status, message, encode=True): #encode true: formato json, false: formato python (puedo manipularlo)
	res = {
		"status": status,
		"message": message,
		"data": []
	}

	return json.dumps(res) if encode else res

def areDatesDifferences90days(dateSince, dateTo):
	days90 = 86400*90 #90 dias en unix
	Dif = float(dateTo) - float(dateSince)
	#resultado = Dif/86400 #BORRAR (dias de diferencia)
	if Dif <= days90:
		return True
	else:
		return False       
	
def areValidDatesInputUnix(date1, date2):
	try: 
		t1 = time.strftime("%Y-%m-%d", time.localtime(date1)) #convierto unix a datetime
		t2 = time.strftime("%Y-%m-%d", time.localtime(date2))
	except:
		return getResponseJson("error", "Dates must be in unix format", False)

	return getResponseJson("success", "Ok", False)

def orderDictionary(dic):
	dic_parseado = {} #primero se convierte los string en int (ya que son numeros, para poder ordenarlos.)
	for key in dic:
		key_parsed = int(key)
		dic_parseado[key_parsed] = dic[key]
	return dic_parseado

#TIPOS DE METODOS CON CARACTERISTICAS COMUNES
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
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)                        
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

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
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

def typeMethodNumberOf(method_name): #Datos agrupados por numero de.. (personas, veces, clicks, milisegundos)
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
								value = values["value"] #value (nro de personas)
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								jRes.append(
								{
									fecha: value
								})
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)                                  
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

def typeMethodTypeOf(method_name): #Datos agrupados por tipo de.. (reacciones, num. de veces, etc)
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
					url = buildUrl(graphUrl,token, method_name, jsonData["date_since"], jsonData["date_until"])
					req = requests.get(url)
					res = json.loads(req.text)
					jRes = [] #lista de datos que se muestran en json response
					for data in res["data"]:
						if data["period"] == "day":
							for values in data["values"]:
								value = values["value"] #value (nro de personas)
								fecha_temp = values["end_time"].split('T') #end_time
								fecha = fecha_temp[0]
								jRes.append(
								{
									fecha: value
								})
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

def typeMethodTypeOfOrdered(method_name): #Datos agrupados y ordenados por tipo de.. (reacciones, num. de veces, etc)
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
								dic_info = {}
								claves = values["value"].keys()                       
								for c in claves: 
									valor_dato = values["value"][c] #valor de la clave 1, valor de la clave 2..
									clave_dato = c
									dic_info[clave_dato] = valor_dato
								dic_resultado = orderDictionary(dic_info)
								jRes.append({
									fecha: dic_resultado                                     
								})
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)    
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

def typeMethodPostsVideos(method_name): #Numero de visitas a post o reproducciones de videos (VER)
	try:
		isValid = isValidJsonData(request)
		if isValid:
			jsonData = request.get_json()
			validArgs = areValidPostArguments(jsonData, ["account", "date_since", "date_until", "posts"])
			if validArgs["status"] == "error":
				return json.dumps(validArgs)
			if areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
				if areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
					res_token = getToken(jsonData["account"])
					token = res_token["message"]
					pageId = getPageId(token)
					jRes = [] #lista de datos que se muestran en json response
					for post in jsonData["posts"]:
						url = buildUrlPost(pageId, post, token, method_name, jsonData["date_since"], jsonData["date_until"])
						print(url)
						req = requests.get(url)
						res = json.loads(req.text)
						for data in res["data"]:
							for value in data["values"]:
								valor_dato = value["value"]                       
								jRes.append({
									post : valor_dato  #idPost : valor
								})
					jsonResponse = getResponseJson("success", "", False)
					jsonResponse["data"] = jRes
					return json.dumps(jsonResponse)
				else:
					return getResponseJson("error", "The maximum range is 90 days", False)
		else:
			return getResponseJson("error", "Invalid data format or not data available")
	except:
		setLog()
		return getResponseJson("error", "Programming failure")

#GRUPO DE METODOS GENERO-EDAD 
@app.route('/getPageContentActivityByAgeGenderUnique', methods=['POST'])
def page_content_activity_by_age_gender_unique():
	return typeMethodGenderAge("page_content_activity_by_age_gender_unique") 

@app.route('/getPageImpressionsByAgeGenderUnique', methods=['POST'])
def page_impressions_by_age_gender_unique():
	return typeMethodGenderAge("page_impressions_by_age_gender_unique")

@app.route('/getPageFansGenderAge', methods=['POST'])
def page_fans_gender_age():
	return typeMethodGenderAge("page_fans_gender_age")


#GRUPO DE METODOS POR CIUDAD 
@app.route('/getPageFansCity', methods=['POST'])
def page_fans_city():
   return typeMethodCity("page_fans_city")

@app.route('/getPageImpressionsByCityUnique', methods=['POST'])
def page_impressions_by_city_unique():
	return typeMethodCity("page_impressions_by_city_unique")


#GRUPO DE METODOS POR NUMERO DE..
@app.route('/getPageImpressionsUnique', methods=['POST'])
def page_impressions_unique():
	return typeMethodNumberOf("page_impressions_unique")

@app.route('/getPageImpressionsPaidUnique', methods=['POST'])
def page_impressions_paid_unique():
	return typeMethodNumberOf("page_impressions_paid_unique")

@app.route('/getPageImpressionsOrganicUnique', methods=['POST'])
def page_impressions_organic_unique():
	return typeMethodNumberOf("page_impressions_organic_unique")

@app.route('/getPagePostEngagements', methods=['POST'])
def page_post_engagements():
	return typeMethodNumberOf("page_post_engagements")

@app.route('/getPageEngagedUsers', methods=['POST'])
def page_engaged_users():
	return typeMethodNumberOf("page_engaged_users")

@app.route('/getPageConsumptionsUnique', methods=['POST'])
def page_consumptions_unique():
	return typeMethodNumberOf("page_consumptions_unique")

@app.route('/getPageNegativeFeedbackUnique', methods=['POST'])
def page_negative_feedback_unique ():
	return typeMethodNumberOf("page_negative_feedback_unique")

@app.route('/getPageTotalActions', methods=['POST'])
def page_total_actions():
	return typeMethodNumberOf("page_total_actions")

@app.route('/getPageFans', methods=['POST'])
def page_fans():
	return typeMethodNumberOf("page_fans") 

@app.route('/getPageFanAdds', methods=['POST'])
def page_fan_adds():
	return typeMethodNumberOf("page_fan_adds")

@app.route('/getPageFanAddsUnique', methods=['POST'])
def page_fan_adds_unique():
	return typeMethodNumberOf("page_fan_adds_unique")

@app.route('/getPageFanRemovesUnique', methods=['POST'])
def page_fan_removes_unique():
	return typeMethodNumberOf("page_fan_removes_unique")

@app.route('/getPageViewsTotal', methods=['POST'])
def page_views_total():
	return typeMethodNumberOf("page_views_total") 

@app.route('/getPageVideoViews', methods=['POST'])
def page_video_views():
	return typeMethodNumberOf("page_video_views")

@app.route('/getPageVideoViewsClickToPlay', methods=['POST'])
def page_video_views_click_to_play():
	return typeMethodNumberOf("page_video_views_click_to_play")   

@app.route('/getPageVideoViewTime', methods=['POST'])
def page_video_view_time():
	return typeMethodNumberOf("page_video_view_time")    

@app.route('/getPagePostsImpressions', methods=['POST'])
def page_posts_impressions():
	return typeMethodNumberOf("page_posts_impressions")  

@app.route('/getPagePostsImpressionsUnique', methods=['POST'])
def page_posts_impressions_unique():
	return typeMethodNumberOf("page_posts_impressions_unique") 

@app.route('/getPagePostsImpressionsPaid', methods=['POST'])
def page_posts_impressions_paid():
	return typeMethodNumberOf("page_posts_impressions_paid") 

@app.route('/getPagePostsImpressionsPaidUnique', methods=['POST'])
def page_posts_impressions_paid_unique():
	return typeMethodNumberOf("page_posts_impressions_paid_unique") 

@app.route('/getPagePostsImpressionsOrganic', methods=['POST'])
def page_posts_impressions_organic():
	return typeMethodNumberOf("page_posts_impressions_organic")

@app.route('/getPagePostsImpressionsOrganicUnique', methods=['POST'])
def page_posts_impressions_organic_unique():
	return typeMethodNumberOf("page_posts_impressions_organic_unique")


#GRUPO DE METODOS POR PUBLICACIONES Y VIDEOS
@app.route('/getPostImpressions', methods=['POST'])
def post_impressions():
	return typeMethodPostsVideos("post_impressions") 
@app.route('/getPostImpressionsUnique', methods=['POST'])
def post_impressions_unique():
	return typeMethodPostsVideos("post_impressions_unique") 
@app.route('/getPostImpressionsPaid', methods=['POST'])
def post_impressions_paid():
	return typeMethodPostsVideos("post_impressions_paid")
@app.route('/getPostImpressionsPaidUnique', methods=['POST'])
def post_impressions_paid_unique():
	return typeMethodPostsVideos("post_impressions_paid_unique")
@app.route('/getPostImpressionsOrganic', methods=['POST'])
def post_impressions_organic():
	return typeMethodPostsVideos("post_impressions_organic") 
@app.route('/getPostImpressionsOrganicUnique', methods=['POST'])
def post_impressions_organic_unique():
	return typeMethodPostsVideos("post_impressions_organic_unique") 
@app.route('/getPostEngagedUsers', methods=['POST'])
def post_engaged_users():
	return typeMethodPostsVideos("post_engaged_users")
@app.route('/getPostNegativeFeedbackByTypeUnique', methods=['POST'])
def post_negative_feedback_by_type_unique():
	return typeMethodPostsVideos("post_negative_feedback_by_type_unique") 
@app.route('/getPostEngagedFan', methods=['POST'])
def post_engaged_fan():
	return typeMethodPostsVideos("post_engaged_fan") 
@app.route('/getPostVideoCompleteViewsOrganicUnique', methods=['POST'])
def post_video_complete_views_organic_unique():
	return typeMethodPostsVideos("post_video_complete_views_organic_unique")
@app.route('/getPostVideoCompleteViewsPaidUnique', methods=['POST'])
def post_video_complete_views_paid_unique():
	return typeMethodPostsVideos("post_video_complete_views_paid_unique")
@app.route('/getPostVideoViewsOrganic', methods=['POST'])
def post_video_views_organic():
	return typeMethodPostsVideos("post_video_views_organic")
@app.route('/getPostVideoViewsOrganicUnique', methods=['POST'])
def post_video_views_organic_unique():
	return typeMethodPostsVideos("post_video_views_organic_unique")
@app.route('/getPostReactionsByTypeTotal', methods=['POST'])
def post_reactions_by_type_total():
	return typeMethodPostsVideos("post_reactions_by_type_total")


#GRUPO DE METODOS POR TIPO DE.. 
@app.route('/getPageImpressionsFrequencyDistribution', methods=['POST'])
def page_impressions_frequency_distribution():
	return typeMethodTypeOf("page_impressions_frequency_distribution")

@app.route('/getPagePositiveFeedbackByTypeUnique', methods=['POST'])
def page_positive_feedback_by_type_unique():
	return typeMethodTypeOf("page_positive_feedback_by_type_unique")

@app.route('/getPageFanAddsByPaidNonPaidUnique', methods=['POST'])
def page_fan_adds_by_paid_non_paid_unique():
	return typeMethodTypeOf("page_fan_adds_by_paid_non_paid_unique")

@app.route('/getPageActionsPostReactionsTotal', methods=['POST'])
def page_actions_post_reactions_total():
	return typeMethodTypeOf("page_actions_post_reactions_total")

@app.route('/getPageFansByUnlikeSourceUnique', methods=['POST'])
def page_fans_by_unlike_source_unique():
	return typeMethodTypeOf("page_fans_by_unlike_source_unique")

@app.route('/getPageViewsExternalReferrals', methods=['POST'])
def page_views_external_referrals ():
	return typeMethodTypeOf("page_views_external_referrals") 

@app.route('/getPageVideoViewsByPaidNonPaid', methods=['POST'])
def page_video_views_by_paid_non_paid():
	return typeMethodTypeOf("page_video_views_by_paid_non_paid") 
  
@app.route('/getPagePostsImpressionsFrequencyDistribution', methods=['POST'])
def page_posts_impressions_frequency_distribution():
	return typeMethodTypeOf("page_posts_impressions_frequency_distribution") 

@app.route('/getPageMessagesTotalMessagingConnections', methods=['POST'])
def page_messages_total_messaging_connections():
	return typeMethodTypeOf("page_messages_total_messaging_connections")

@app.route('/getPageMessagesNewConversationsUnique', methods=['POST'])
def page_messages_new_conversations_unique():
	return typeMethodTypeOf("page_messages_new_conversations_unique")

@app.route('/getPageMessagesBlockedConversationsUnique', methods=['POST'])
def page_messages_blocked_conversations_unique():
	return typeMethodTypeOf("page_messages_blocked_conversations_unique")

@app.route('/getPageMessagesReportedConversationsUnique', methods=['POST'])
def page_messages_reported_conversations_unique():
	return typeMethodTypeOf("page_messages_reported_conversations_unique")

#GRUPO DE METODOS POR TIPO ORDENADO DE..
@app.route('/getPageFansOnline', methods=['POST'])
def page_fans_online():
	return typeMethodTypeOfOrdered("page_fans_online")

if __name__ == '__main__':
	try:
		reload(sys)
		sys.setdefaultencoding('utf8')
		serve(app, host='0.0.0.0', port=5001)
	except:
		setLog()
