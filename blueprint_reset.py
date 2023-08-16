from functools import partial
import json
from re import sub
from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
import csv
import os
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map


# API Keys from JSON object
with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

# api entry points/keys
# test instance API_KEY
API_KEY = keys['prod']
API_URL = "https://cms.instructure.com"
# instantiate Canvas object
canvas = Canvas(API_URL, API_KEY)


fix = []
with open('fix_blueprint_cte.csv', 'r') as sis_fix:
    csv_read = csv.DictReader(sis_fix)
    fix = [r for r in csv_read]

for f in fix:
    f_sis = f['course_id']
    course = canvas.get_course(f_sis,use_sis_id=True)
    print(course.reset())
