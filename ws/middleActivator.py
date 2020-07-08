import os
import signal
import inspect
import traceback
import sys
import requests
import time
import simplejson as json
import subprocess
from waitress import serve
from flask import Flask
from flask import request
from datetime import date, datetime
from time import gmtime, strftime

app = Flask(__name__)
logs_path = "D:\\eniac\\LABS357 Dashboard\\Webservices LABS\\ws\\logs\\"
classes_path = "D:\\eniac\\LABS357 Dashboard\\Webservices LABS\\ws\\classes\\"

def setLog():
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = repr(traceback.format_exception("", exc_value, exc_traceback))
        origin = inspect.stack()[1][3]
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
        with open(logs_path + "activator.log", "a") as logFile:
            logFile.write(stringError)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = repr(traceback.format_exception("", exc_value, exc_traceback))
        origin = inspect.stack()[1][3]  
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
        with open(logs_path + "activator.log", "a") as logFile:
            logFile.write(stringError)

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

def getResponseJson(status, message, encode=True): #encode true: formato json, false: formato python (puedo manipularlo)
    res = {
        "status": status,
        "message": message,
        "data": []
    }

    return json.dumps(res) if encode else res

def areValidPostArguments(jsonData, args):
    invalidArgs = []
    for a in args:
        if a not in jsonData:
            invalidArgs.append(a)

    if (len(invalidArgs) > 0):
        return getResponseJson("error", "The following arguments are required: " + ", ".join(invalidArgs), False) 
    else:
        return getResponseJson("success", "Ok", False)     

@app.route('/activate', methods=['POST']) 
def activator():
    try:
        isValid = isValidJsonData(request)
        data = tuple
        if isValid:
            jsonData = request.get_json()
            validArgs = areValidPostArguments(jsonData, ["account" , "connection_id", "metrics"])
            if validArgs["status"] == "error":
                return app.response_class(response=json.dumps(validArgs),mimetype='application/json')
            result = subprocess.Popen(['python', classes_path + 'middle.py', json.dumps(jsonData), "activate", "&"])
            return app.response_class(response=getResponseJson("success", "The script activation request has been sent."),mimetype='application/json')
        else:
            return app.response_class(response=getResponseJson("error", "Invalid data format or not data available"),mimetype='application/json')
    except:
        setLog()     
        return app.response_class(response=getResponseJson("error", "Programming failure"),mimetype='application/json')

@app.route('/deactivate', methods=['POST'])
def deactivator(): #Detener script de middle corriendo en la pc. 
    try:
        isValid = isValidJsonData(request)
        if isValid:
            jsonData = request.get_json()
            validArgs = areValidPostArguments(jsonData, ["account"])
            if validArgs["status"] == "error":
                return app.response_class(response=json.dumps(validArgs),mimetype='application/json')
            result = subprocess.Popen(['python', classes_path + 'middle.py', json.dumps(jsonData), "deactivate"])
            return app.response_class(response=getResponseJson("success", "The script deactivation request has been sent."),mimetype='application/json')
        
        else:
            return app.response_class(response=getResponseJson("error", "Invalid data format or not data available"),mimetype='application/json')
    except:
        setLog()
        return app.response_class(response=getResponseJson("error", "Programming failure"),mimetype='application/json')

if __name__ == '__main__':
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
        serve(app, host='0.0.0.0', port=5002)
    except:
        setLog()