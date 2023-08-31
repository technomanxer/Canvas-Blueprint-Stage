import datetime
from functools import partial
import json
from re import sub
from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
import csv
import os
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import requests
import time

with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

headers={
    'Authorization': "Bearer " + keys['prod']
}

req = requests.post('https://cms.instructure.com/api/v1/accounts/1446/reports/sis_export_csv', params={'parameters[courses]': True}, headers=headers)
json_re = req.json()
time.sleep(10)

id = json_re['id']
print("report " + str(id))

#check url
done = False
file_url=""
while(not done):
    req = requests.get('https://cms.instructure.com/api/v1/accounts/1446/reports/sis_export_csv/'+str(id), headers=headers)
    print("not done yet, sleeping for 30 secs")
    if(req.json()['status'] == 'complete'):
        file_url = req.json()['attachment']['url']
        break
    time.sleep(30)

#download url
req = requests.get(file_url)
open("sis_export.csv", 'wb').write(req.content)

need_blueprint=[]
with open('course_codes.csv') as csvfile:
    read = csv.reader(csvfile)
    need_blueprint=[x for x in read if x[-1]]


#dictionary formation 
associate = dict()
for rows in need_blueprint:
    associate[rows[0]] = rows[-1]

associate['99329X0900'] = 'titleixhs' #homeroom HS
associate['99329Y0900'] = 'titleixms' #homeroom MS

#feed bp file
no_assoc = []
with open('sis_export.csv') as sis_file:
    read = csv.DictReader(sis_file)
    no_assoc = [x for x in read if x['blueprint_course_id'] == ""]

#course code: no_assoc[0]['short_name'][-11:-1]
sis_import = []

for c in no_assoc:
    course_code = c['short_name'][-11:-1]
    if course_code in associate.keys():
        c['blueprint_course_id'] = "bp_" + associate[course_code]
        sis_import.append(c)

filename='sis_import_'+str(datetime.date.today())+'.csv'
with open(filename, 'w',  newline="") as import_file:
    write_f = csv.DictWriter(import_file, fieldnames=sis_import[0].keys())
    write_f.writeheader()
    write_f.writerows(sis_import)

# to do write code to upload

file_send = {"attachment": open(filename, 'rb')}
req = requests.post("https://cms.instructure.com/api/v1/accounts/1/sis_imports", headers=headers, files=file_send)
print(req.json())