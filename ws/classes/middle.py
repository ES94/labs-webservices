import os
import signal
import sys
import shelve
import time
import requests
import subprocess
import simplejson as json
import inspect
import traceback
from flask import Flask
from datetime import date, datetime

app = Flask(__name__)

process_update_time = 2 #tiempo de actualizacion de las metricas en segundos.
process_max_time = 20 #tiempo en segundos maximo de ejecucion de un proceso.
logs_path = "D:\\eniac\\LABS357 Dashboard\\Webservices LABS\\ws\\logs\\"
db_path = "D:\\eniac\\LABS357 Dashboard\\Webservices LABS\\ws\\databases\\"

def getResponseJson(status, message, encode=True): #encode true: formato json, false: formato python (puedo manipularlo)
    res = {
        "status": status,
        "message": message,
        "data": []
    }

    return json.dumps(res) if encode else res

def setLog():
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = repr(traceback.format_exception("", exc_value, exc_traceback))
        origin = inspect.stack()[1][3]
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
        with open(logs_path + "middle.log", "a") as logFile:
            logFile.write(stringError)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = repr(traceback.format_exception("", exc_value, exc_traceback))
        origin = inspect.stack()[1][3]  
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        stringError = str(time) + " --- " + str(origin) + ": " + str(error) + "\n"
        with open(logs_path + "middle.log", "a") as logFile:
            logFile.write(stringError)

class Middle():
    
    _host = "127.0.0.1"
    _port = 5001

    @staticmethod
    def savePid(account):
        try:
            dic = {}
            pid = str(os.getpid()) #Obtengo el PID
            dic = shelve.open(db_path + 'middlePids.db')
            key = account
            dic[str(key)] = pid
            #print "PID GUARDADO: ",pid
            dic.close()
        except:
            setLog()
        return None
    
    @staticmethod
    def getPid(account):
        try:
            dic = {}
            dic = shelve.open(db_path + 'middlePids.db')
            pid = None
            for key in dic:
                if str(account) == str(key):
                    pid = dic[key]
        except:
            setLog()
        return pid

    @staticmethod
    def removePid(account):
        try:
            dic = {}
            dic = shelve.open(db_path + 'middlePids.db')
            pid = None
            for key in dic:
                if str(account) == str(key):
                    temp = key
                    del dic[key]
        except:
            setLog()
        
    @staticmethod
    def getMetrics(jsonData):
        metrics_list = []
        try:
            host = Middle._host
            port = Middle._port
            for metric in jsonData["metrics"]:
                metric_name = metric["metric_name"].title()
                metric_name = metric_name.replace("_","")
                url = "http://" + str(host) + ":" + str(port) + "/" + "get" + metric_name
                hayPosts = False
                for key in metric:
                    if str(key) == "posts":
                        hayPosts = True 
                if (hayPosts): #En caso que utilice metricas de videos (reciben el parametro posts adicionalmente)
                    data = {'account': jsonData["account"], 'date_since': metric["date_since"], 'date_until': metric["date_until"], 'posts': metric["posts"]}
                else:
                    data = {'account': jsonData["account"], 'date_since': metric["date_since"], 'date_until': metric["date_until"]}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                req = requests.post(url, data=json.dumps(data), headers=headers)
                if (req != None):
                    res = json.loads(req.text) 
                    metrics_list.append(res["data"])
        except:
            setLog()
        return metrics_list

    @staticmethod
    def activate(jsonData):
        try:
            urlDashboard = "http://labs357.com.ar/dbTest.php"
            headersDashboard = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            Middle.savePid(jsonData["account"]) #Guardo el id de proceso
            pid = Middle.getPid(jsonData["account"])
            start_time = time.time()
            available_time = 0            
            while (pid != None and available_time < process_max_time): #Mientras que exista el PID en el archivo pids.db 
                #print available_time
                metricsDashboard = Middle.getMetrics(jsonData)
                if metricsDashboard is None:
                    return app.response_class(response=getResponseJson("error", "Metrics not found or not available." , False),mimetype='application/json')
                else:
                    jsonResponse = getResponseJson("success", "", False)
                    jsonResponse["data"] = {"connection_id":jsonData["connection_id"], "metrics":metricsDashboard}
                    response = app.response_class(response=jsonResponse,mimetype='application/json')
                    responseFinal = response.response
                    reqDashboard =  requests.post(urlDashboard, data=json.dumps(responseFinal), headers=headersDashboard)
                time.sleep(process_update_time)
                pid = Middle.getPid(jsonData["account"])
                end_time = time.time()
                available_time = end_time - start_time
        except:
            setLog()
        if (available_time >= process_max_time):
            Middle.deactivate(jsonData["account"])
        return None

    @staticmethod
    def deactivate(account):
        try:
            pid = None
            pid = Middle.getPid(account)
            if pid is None:
                return getResponseJson("error", "The process ID for the specified account was not found" , False)        
            else:
                os.kill(int(pid), 9) #SIGKILL no soportado en windows.
                Middle.removePid(account) #Esto desencadenara la detencion de la instancia middle creada anteriormente.
        except:
            setLog()
        return None

if __name__ == '__main__':
    jsonD = json.loads(sys.argv[1]) #JSON: account, connection_id, metrics
    is_activanding = sys.argv[2] #"activate" / "deactivate"
    if is_activanding == "activate":
        Middle.activate(jsonD)
    else:
        Middle.deactivate(jsonD["account"])