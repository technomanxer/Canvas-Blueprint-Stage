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

need_blueprint=[]
with open('course_code.csv') as csvfile:
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

with open('sis_import_'+str(datetime.date.today())+'.csv', 'w',  newline="") as import_file:
    write_f = csv.DictWriter(import_file, fieldnames=sis_import[0].keys())
    write_f.writeheader()
    write_f.writerows(sis_import)
