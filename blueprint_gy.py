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
API_URL = "insert instance URL here"
# instantiate Canvas object
canvas = Canvas(API_URL, API_KEY)

def blueprint_move(course_obj):
    # kwarg course object to change, we need to change account ID and term
    course_changes = {
        'term_id': '1316',  # default term
        'account_id': '2414'
    }
    tqdm.write("moving course " + course_obj.name)
    return course_obj.update(course=course_changes)



powerschool = canvas.get_account(1446)
bp_old = powerschool.get_courses(blueprint=True)

results = thread_map(blueprint_move, bp_old, max_workers=5, unit="courses", desc="moving blueprint courses...", colour='green')

