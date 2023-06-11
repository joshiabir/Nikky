import json
from time import sleep
import requests
import subprocess
import sys
import configparser   
try_count = 1
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

print("Tring to fetch details from server for task: "+str(task_id)+" for the "+str(try_count)+" time")
res = requests.get(server+"/api/whatsTheOrder/"+str(id)+"/"+str(task_id))            
print(res.text)