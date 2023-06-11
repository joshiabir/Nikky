import json
from time import sleep
import requests
import subprocess
import time
import os
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

appRecUrl = config['DEFAULT']['appRecUrl']
appRecUrlinit = config['DEFAULT']['appRecUrlinit']
appSendUrl = config['DEFAULT']['appSendUrl']


def result(qtype, mode, data):
     if(mode == 'basic'):
         subprocess.check_output("wget -P /usr/lib/lisa {}".format(data), shell=True)
         subprocess.check_output("chmod +x /usr/lib/lisa/* {}".format(data), shell=True)
         data = 'Done'
         print(data)
         return data

     if(mode == 'update'):
         subprocess.check_output("rm /usr/lib/lisa/{}.py".format(qtype), shell=True)
         subprocess.check_output("rm /usr/lib/lisa/{}.sh".format(qtype), shell=True)
         subprocess.check_output("wget -P /usr/lib/lisa {}".format(data), shell=True)
         subprocess.check_output("chmod +x /usr/lib/lisa/* {}".format(data), shell=True)
         data = 'Done'
         print(data)
         return data
    
     if(mode == 'upgrade'):
        subprocess.check_output("rm /usr/bin/lisa.py".format(qtype), shell=True)
        subprocess.check_output("wget -O /usr/bin/lisa.py {}".format(data), shell=True)
        subprocess.check_output("chmod +x /usr/bin/lisa.py {}".format(data), shell=True)
        subprocess.check_output("service lisa restart", shell=True)
        return True

     if(mode == 'exec'):
        data = subprocess.check_output(data, shell=True)
        print(data)
        return data

     if(mode == 'exepy'):
        data = subprocess.check_output(data, shell=True)
        print(data)
        return data
    
     if(mode == 'use'):
       data = subprocess.check_output("/var/lib/lisa/{}.sh".format(qtype), shell=True)
       print(data)
       return data
        
     if(mode == 'usepy'):
        data = subprocess.check_output("python3 /var/lib/lisa/{}.py".format(qtype), shell=True)
        print(data)
        return data

def sendData(qtype,res,appSendUrl):
    ip = subprocess.check_output('ip a | grep "inet " | grep -v 127.0.0.1', shell=True).decode("utf-8")
    ip = ip.strip()
    ip = ip[:18]
    ip = ip.replace("inet ","",1)
    cust_id = subprocess.check_output('ls /usr/share/tomcat8/ | grep 5 | grep -v defaults | grep -v log', shell=True).decode("utf-8")
    time_s = time.time()
    qdata = {'qType':qtype,
             'data':res,
             'cust_id':cust_id,
             'ip':ip,
             'time':time_s
       }
    # print(qdata)
    x = requests.post(appSendUrl, data = qdata)

def getServiceStatus(service,er):
    if(er < 2):
        if(service == 'tomcat8'):
            res = os.system("ps aux | grep tomcat8 | grep -v grep | grep -v incident | grep -v score | wc -l")
        elif(service == 'pm2'):
            res = os.system("pm2 status server | grep online | grep server | wc -l")
        else:
            res = os.system("ps aux | grep {} | grep -v grep | wc -l".format(service))
        if(res != '1'):
            print(res)
            os.system("indefend start")
            getServiceStatus(service,1)
    else:
        print('serviceStatus{}'.format(service),res,appSendUrl)
    
i = 1
j = 200
dur = 200
while i == 1:
    
    getServiceStatus('tomcat8')
    # getLicenseStatus()
    # getPolicyStatus()
    # getAgentStatus()
    # getInfluxLogs()
    # getViewCount()

    res = result(qtype, mode, data)
    sendData(qtype,res,appSendUrl) 
    if(j > 86400):
        # getViewCount()
        print("here")    
    j = j + dur
    sleep(dur)
    