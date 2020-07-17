#!/usr/bin/python
# -*- coding: utf-8 -*-

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

from .settings import Settings
from classes.database import Database


host = Settings.host
user = Settings.user
pswd = Settings.pswd


class Utils:
    @staticmethod
    def getPageId(graphUrlId, token):
    	url = graphUrlId + "access_token=" + token 
    	req = requests.get(url)
    	res = json.loads(req.text)
    	name = res["name"]
    	pageId = res["id"]
    	return pageId

    @staticmethod
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

    @staticmethod
    def buildUrl(baseUrl, token, metric, date_since, date_until):
    	return baseUrl + "access_token=" + token + "&metric=" + metric + "&since=" + str(date_since) + "&until=" + str(date_until)

    @staticmethod
    def computeMD5hash(my_string):
    	m = hashlib.md5()
    	m.update(my_string.encode('utf-8'))
    	return m.hexdigest()

    @staticmethod
    def getToken(host, user, pswd, account):
    	DATABASE = Database.getInstance(host,user,pswd,"dev_plataforma")
    	query = "SELECT I.password FROM instancias I"
    	query = query + " WHERE I.id_medio = 2"
    	query = query + " and I.id_cuenta =" + str(account)
    
    	res = DATABASE.executeQuery(query, None, True)
    	if res is not None and len(res) == 1: #Deberia haber solo una cuenta con ese ID
    		token = res[0][0]
    		return Utils.getResponseJson("success", token, False) 
    	else:
    		if res is None:
    			return Utils.getResponseJson("error", "Account not found", False)
    		else:
    			return Utils.getResponseJson("error", "There are many accounts with that id", False)

    @staticmethod
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
    
    @staticmethod
    def areValidPostArguments(jsonData, args):
    	invalidArgs = []
    	for a in args:
    		if a not in jsonData:
    			invalidArgs.append(a)

    	if (len(invalidArgs) > 0):
    		return Utils.getResponseJson("error", "The following arguments are required: " + ", ".join(invalidArgs), False)
    	else:
    		return Utils.getResponseJson("success", "Ok", False)
    
    @staticmethod
    def areValidGetArguments(request, args):
    	invalidArgs = []
    	for a in args:
    		if request.args.get(a) is None:
    			invalidArgs.append(a)

    	if (len(invalidArgs) > 0):
    		return Utils.getResponseJson("error", "The following arguments are required: " + ", ".join(invalidArgs), False)
    	else:
    		return Utils.getResponseJson("success", "Ok", False)

    @staticmethod
    def getResponseJson(status, message, encode=True): #encode true: formato json, false: formato python (puedo manipularlo)
    	res = {
    		"status": status,
    		"message": message,
    		"data": []
    	}

    	return json.dumps(res) if encode else res

    @staticmethod
    def areDatesDifferences90days(dateSince, dateTo):
    	days90 = 86400*90 #90 dias en unix
    	Dif = float(dateTo) - float(dateSince)
    	#resultado = Dif/86400 #BORRAR (dias de diferencia)
    	if Dif <= days90:
    		return True
    	else:
    		return False       
    
    @staticmethod
    def areValidDatesInputUnix(date1, date2):
    	try: 
    		t1 = time.strftime("%Y-%m-%d", time.localtime(date1)) #convierto unix a datetime
    		t2 = time.strftime("%Y-%m-%d", time.localtime(date2))
    	except:
    		return Utils.getResponseJson("error", "Dates must be in unix format", False)

    	return Utils.getResponseJson("success", "Ok", False)

    @staticmethod
    def orderDictionary(dic):
    	dic_parseado = {} #primero se convierte los string en int (ya que son numeros, para poder ordenarlos.)
    	for key in dic:
    		key_parsed = int(key)
    		dic_parseado[key_parsed] = dic[key]
    	return dic_parseado