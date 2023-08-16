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


def blueprint_set(course_obj):
    print(course_obj.id)
    # kwarg course object to change, we need to change account ID and term
    course_changes = {
        'term_id': '1316',  # default term
        'blueprint': True
    }
    # print("TEST MOVED " + str(course_obj.id))
    return course_obj.update(course=course_changes)

def blueprint_move(course_obj):
    print(course_obj.id)
    # kwarg course object to change, we need to change account ID and term
    course_changes = {
        'account_id': '1446'
    }
    # print("TEST MOVED " + str(course_obj.id))
    return course_obj.update(course=course_changes)


def sis_id_set(course_obj):
    sis_id = "bp_"+str(course_obj.id)
    course_changes = {
        'sis_course_id': sis_id
    }
    # print("TEST MOVED " + str(course_obj.id))
    return course_obj.update(course=course_changes)

# account = canvas.get_account(2385).get_subaccounts()
# for sub in account:
#     courses = sub.get_courses()
#     courses = [x for x in courses if x.sis_course_id is None]
#     for x in courses:
#         sis_id_set(x)


account = canvas.get_account(2385).get_courses(blueprint=True)
for c in account:
    print(blueprint_move(c))