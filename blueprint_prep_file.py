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

#Edit the request so that your URL is used 

req = requests.post('https:/<insert URL here>/api/v1/accounts/1446/reports/sis_export_csv', params={'parameters[courses]': True}, headers=headers)
json_re = req.json()
time.sleep(10)

id = json_re['id']
print("report " + str(id))

#check url for if the report is done.
done = False
file_url=""
while(not done):
    req = requests.get('https://<insert URL here>/api/v1/accounts/1446/reports/sis_export_csv/'+str(id), headers=headers)
    print("not done yet, sleeping for 30 secs")
    if(req.json()['status'] == 'complete'):
        file_url = req.json()['attachment']['url']
        break
    time.sleep(30)

#download the report!
req = requests.get(file_url)
open("sis_export.csv", 'wb').write(req.content)


#Pull courses that have blueprints associated.
#see course_codes.csv for blueprint file mapping
need_blueprint=[]
with open('course_codes.csv') as csvfile:
    read = csv.reader(csvfile)
    need_blueprint=[x for x in read if x[-1]]


#dictionary formation {course_code: blueprint}
associate = dict()
for rows in need_blueprint:
    associate[rows[0]] = rows[-1]

#Use this area to put in custom course codes and blueprints. Or add to the file course_codes.CSV
#associate['99329X0900'] = 'titleixhs' #homeroom HS
#associate['99329Y0900'] = 'titleixms' #homeroom MS

#This now reads the export file and determines who needs a blueprint association
no_assoc = []
with open('sis_export.csv') as sis_file:
    read = csv.DictReader(sis_file)
    no_assoc = [x for x in read if x['blueprint_course_id'] == ""]

#course code: no_assoc[0]['short_name'][-11:-1]
sis_import = []

# now we write the association into the end of the line in the CSV and output a new file called "sis_import"
for c in no_assoc:
    course_code = c['short_name'][-11:-1]
    if course_code in associate.keys():
        c['blueprint_course_id'] = "bp_" + associate[course_code]
        sis_import.append(c)

#write to import file with today's date
filename='sis_import_'+str(datetime.date.today())+'.csv'
with open(filename, 'w',  newline="") as import_file:
    write_f = csv.DictWriter(import_file, fieldnames=sis_import[0].keys())
    write_f.writeheader()
    write_f.writerows(sis_import)

# Uploads file to Canvas instance
file_send = {"attachment": open(filename, 'rb')}
req = requests.post("https://<insert instance here>/api/v1/accounts/1/sis_imports", headers=headers, files=file_send)
print(req.json())
