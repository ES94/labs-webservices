import requests
import simplejson as json
from flask import request

from classes.settings import Settings
from classes.utils import Utils


graphUrl = "https://graph.facebook.com/v4.0/me/insights?"
graphUrlPosts = "https://graph.facebook.com/v4.0/me/posts?"
graphUrlVideos = "https://graph.facebook.com/v4.0/me/videos?"
graphUrlId = "https://graph.facebook.com/v4.0/me?"


class Facebook:
    def buildUrlPost(self, pageId, postId, token, metric, date_since, date_until):
    	return "https://graph.facebook.com/v4.0/" + pageId + "_" + postId + "/insights?" + "access_token=" + token + "&metric=" + metric + "&since=" + str(date_since) + "&until=" + str(date_until)
    
    @staticmethod
    def typeMethodCity(method_name): #Datos agrupados por ciudad
    	try:
    		isValid = Utils.isValidJsonData(request)
    		if isValid:
    			jsonData = request.get_json()
    			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
    			if validArgs["status"] == "error":
    					return json.dumps(validArgs)
    			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
    				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
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

    @staticmethod
    def typeMethodGenderAge(method_name): #Datos agrupados por genero en rango de edades.
    	try:
    		isValid = Utils.isValidJsonData(request)
    		if isValid:
    			jsonData = request.get_json()
    			validArgs = Utils.areValidPostArguments(jsonData, ["account" , "date_since", "date_until"])
    			if validArgs["status"] == "error":
    				return json.dumps(validArgs)
    			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):#Chequeo fechas UNIX validas
    				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
    					token = res_token["message"]
    					url = Utils.buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"]) 
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

    @staticmethod
    def typeMethodNumberOf(method_name): #Datos agrupados por numero de.. (personas, veces, clicks, milisegundos)
    	try:
    		isValid = Utils.isValidJsonData(request)
    		if isValid:
    			jsonData = request.get_json()
    			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
    			if validArgs["status"] == "error":
    					return json.dumps(validArgs)
    			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
    				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
    					token = res_token["message"]
    					url = Utils.buildUrl(graphUrl, token, method_name, jsonData["date_since"], jsonData["date_until"])
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

    @staticmethod
    def typeMethodPostsVideos(method_name): #Numero de visitas a post o reproducciones de videos (VER)
    	try:
    		isValid = Utils.isValidJsonData(request)
    		if isValid:
    			jsonData = request.get_json()
    			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until", "posts"])
    			if validArgs["status"] == "error":
    				return json.dumps(validArgs)
    			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
    				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
    					token = res_token["message"]
    					pageId = Utils.getPageId(FbSettings.graphUrlId, token)
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
    					jsonResponse = Utils.getResponseJson("success", "", False)
    					jsonResponse["data"] = jRes
    					return json.dumps(jsonResponse)
    				else:
    					return getResponseJson("error", "The maximum range is 90 days", False)
    		else:
    			return getResponseJson("error", "Invalid data format or not data available")
    	except:
    		Utils.setLog()
    		return Utils.getResponseJson("error", "Programming failure")

    @staticmethod
    def typeMethodTypeOf(method_name): #Datos agrupados por tipo de.. (reacciones, num. de veces, etc)
    	try:
    		isValid = Utils.isValidJsonData(request)
    		if isValid:
    			jsonData = request.get_json()
    			validArgs = Utils.areValidPostArguments(jsonData, ["account", "date_since", "date_until"])
    			if validArgs["status"] == "error":
    					return json.dumps(validArgs)
    			if Utils.areValidDatesInputUnix(jsonData["date_since"], jsonData["date_until"]):
    				if Utils.areDatesDifferences90days(jsonData["date_since"], jsonData["date_until"]):#Chequeo diferencia 90 dias
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
    					token = res_token["message"]
    					url = Utils.buildUrl(graphUrl,token, method_name, jsonData["date_since"], jsonData["date_until"])
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

    @staticmethod
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
    					res_token = Utils.getToken(Settings.DB_HOST, Settings.DB_USER, Settings.DB_PSWD, jsonData["account"])
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