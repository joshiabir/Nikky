import json
from time import sleep
import requests
import subprocess
import sys
import configparser

name = "Carter"

def printl(data):
    print(name+": "+str(data))

def setprams():
    
    global server
    global id
    global retry
    global task_id
    global thread_sleep

    config = configparser.ConfigParser()
    config.read('example.ini')
    
    
    server =  config['carter']['server']
    id = config['carter']['id']
    retry = config['carter']['retry']
    thread_sleep = config['carter']['thread_sleep']
    task_id = sys.argv[1]

def gettingTask(try_count):
    
    printl("Tring to fetch details from server for task: "+str(task_id)+" for the "+str(try_count)+" time")
    res = requests.get(server+"/api/whatsTheOrder/"+id+"/"+task_id)      
    
    printl(server+"/api/whatsTheOrder/"+str(id)+"/"+str(task_id))       
    
    if res.status_code == 200:
        return res
    else:
        sleep(int(thread_sleep))
        if(try_count < int(retry)):
            try_count = try_count+1
            gettingTask(try_count)
        else:
            printl(res.status_code)
            raise SystemExit("Woops we got a stauts code of "+str(res.status_code)+" while connecting to the server")
  

        
def executeTask(payload,type):
    if(type == 'exec'):
        try:
            status = "Good"
            res = subprocess.check_output(payload,shell=True,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            status = "Bad"
            res = ("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

        return res, status

def tellThem(data,status):
    if status == "Good":
        res = requests.post(server+"/api/beenThereDoneThat/", data)
        printl(server+"/api/beenThereDoneThat/")
        printl(data)
    else:
        res = requests.post(server+"/api/beenThereButfailedThat/", data)
        printl(server+"/api/beenThereButfailedThat/")
    
    printl(data)
    printl(res.status_code)


# Creates all global parameters
setprams() 

# Initating the operations
printl("Carter here, up for task ID:{}".format(task_id))

# Getting the task from server
res = gettingTask(int(1))

data = requests.Response.json(res)
printl("We got payload from server: "+str(data))

for p in data:
    payload = p["payload"]
    type = p["type"]

# Executing the payload
out, status = executeTask(payload,type)

# Creating the return back array
data = {
    'id':task_id,
    'app_id':id,
    'out':str(out)
}

# Sending response back to server 
tellThem(data,status)


