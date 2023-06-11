import json
from time import sleep
import requests
import socket
import platform
import psutil
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

server =  config['ginna']['server']
id = config['ginna']['id']


def init():
    
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IPAddr = (s.getsockname()[0])
    processor = platform.processor()
    os = platform.platform()
    cpu_usage = psutil.cpu_percent(5)
    ram_free = psutil.virtual_memory().available/1000000

    data = {
        "Hostname" : hostname,
        "Processor": processor,
        "OS": os,
        "CPU Usage": cpu_usage,
        "Available RAM": ram_free
    }

    data = {"data": json.dumps(data),
            "ip": IPAddr}
    print(data)

    res = requests.post(server+"/api/sup/"+id, data)
    if res.status_code == 200:
        data = requests.Response.json(res)
        print(data)
        for p in data:
         task_id = p["id"]
         app_id = p["app_id"]
         type = p["type"]
         if(type == 'exec') and (app_id == id):
          print("Carter taking over ID:{}".format(task_id))
          res = requests.post(server+"/api/tryingToAssignTask/"+id+"/"+str(task_id))
          print(server+"/api/tryingToAssignTask/"+id+"/"+str(task_id))   
          task_id = int(task_id)
          subprocess.Popen("python3 carter.py {}".format(task_id), shell=True)   
    else:
        print(res.status_code)        

while True:
    init()
    sleep(1)
