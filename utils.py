from itertools import count
import os
import sys
import time

from flask.json import jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import shutil
import base64
import numpy as np
import sqlite3
import json
from dotenv import load_dotenv
import cv2
load_dotenv()


def delete_message(request):
    count = 0
    try:
        message_id = request.form["message_id"]
        count += 1
        room_id = request.form["room_id"]
        count += 1
        time_delete = request.form["time_delete"]
        count += 1
        status_delete = request.form["status_delete"]
        return (
            message_id,
            room_id,
            time_delete,
            status_delete,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def validate(request):
    count = 0
    try:
        username = request.form["username"]
        count += 1
        password = request.form["password"]
        count += 1
        return (
            username,
            password,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def register_user(request):
    count = 0
    try:
        fullname = request.form["fullname"]
        count += 1
        username = request.form["username"]
        count += 1
        password = request.form["password"]
        count += 1
        telephone = request.form["telephone"]
        count += 1
        privateKeyfirst = request.form["privateKeyFirst"]
        count += 1
        image = request.form["avatar"]
        count += 1
        return (
            fullname,
            username,
            password,
            telephone,
            privateKeyfirst,
            image,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count


def send_text(request):
    count = 0
    try:
        personID = request.form["personID"]
        count += 1
        privateKey = request.form["privateKey"]
        count += 1
        text = request.form["text"]
        count += 1
        time = request.form["time"]
        count += 1
        return (
            personID,
            privateKey,
            text,
            time,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def send_message(request):
    count = 0
    try:
        customer_send_info_text = request.form["customer_send_info"]
        count += 1
        user_receive_name = request.form["user_receive_name"]
        count += 1
        customer_send_info_text_image = request.form["customer_send_info_text_image"]
        count += 1
        customer_send_info_text_file = request.form["customer_send_info_text_file"]
        count += 1
        customer_send_info_text_gps = request.form["customer_send_info_text_gps"]
        count += 1
        return (
            customer_send_info_text,
            user_receive_name,
            customer_send_info_text_image,
            customer_send_info_text_file,
            customer_send_info_text_gps,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count

def join_room(request):
    count = 0
    try:
        customer_id = request.form["customer_id_username"]
        count += 1
        user_send_id = request.form["user_send_id"]
        count += 1
        return (
            customer_id,
            user_send_id,
        )
    except Exception as e:
        print(f"Not parse information from request. Error:: {str(e)}")
        return None, count
