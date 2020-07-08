#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as db
import sys
import traceback
import inspect
from datetime import date, datetime

class Database(object):
	__instance = None
	__dbCon = None
	
	@staticmethod
	def getInstance(host, user, pswd, base):
		if Database.__instance == None:
			Database(host, user, pswd, base)
		Database.__instance.host = host
		Database.__instance.user = user
		Database.__instance.pswd = pswd
		Database.__instance.base = base		
		return Database.__instance

	def __init__(self, host, user, pswd, base):
		if Database.__instance == None:
			Database.__instance = self
			self.host = host
			self.user = user
			self.pswd = pswd
			self.base = base
	
	def __setLog(self):
		try:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]

			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(r"D:\eniac\LABS357 Dashboard\Webservices LABS\ws\logs\database.log", "a") as logFile:
				logFile.write(stringError)
		except Exception as e:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			error = repr(traceback.format_exception("", exc_value, exc_traceback))
			origin = inspect.stack()[1][3]
			
			now = datetime.now()
			time = now.strftime("%d/%m/%Y %H:%M:%S")
			stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
			with open(r"D:\eniac\LABS357 Dashboard\Webservices LABS\ws\logs\database.log", "a") as logFile:
				logFile.write(stringError)
	
	def __getConnection(self):
		try:
			if Database.__dbCon == None:
				Database.__dbCon = db.connect(host=self.host,user=self.user,passwd=self.pswd,db=self.base,charset="utf8", init_command="set names utf8")
			
			return Database.__dbCon
		except Exception as e:
			self.__setLog()
			
	def __closeConnection(self):
		try:
			if Database.__dbCon.open:
				Database.__dbCon.close()
			
			Database.__dbCon = None
				
		except Exception as e:
			self.__setLog()
			return None

	def executeQuery(self, query, args, fetch):
		try:
			dbCon 	= self.__getConnection()
			dbCur = dbCon.cursor()
			if args is not None:
				dbCur.execute(query, args)
			else:
				dbCur.execute(query)
			
			if fetch == True:
				res = dbCur.fetchall()
			else:
				res = dbCur.fetchone()
			
			dbCur.close()
			self.__closeConnection()
			return res
		except Exception as e:
			self.__setLog()
			return None
			
	def executeCommand(self, command, args):
		try:
			dbCon 	= self.__getConnection()
			dbCur = dbCon.cursor()
			if args is not None:
				dbCur.execute(command, args)
			else:
				dbCur.execute(command)
				
			dbCur.close()
			dbCon.commit()
			self.__closeConnection()
		except Exception as e:
			self.__setLog()
			return None
			
	def executeManyCommand(self, command, args):
		try:
			dbCon 	= self.__getConnection()
			dbCur = dbCon.cursor()
			dbCur.executemany(command, args)
			
			dbCur.close()
			dbCon.commit()
			self.__closeConnection()
		except Exception as e:
			self.__setLog()
			return None