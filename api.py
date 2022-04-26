import os
import time
import base64
import logging
import sqlite3
import utils
import json
import pandas as pd
import csv
from flask import Flask, request, jsonify
from flask_cors import cross_origin


app = Flask(__name__)


def extract_face():
    message = {"name": "person_id", "sex": "person_type"}
    return message



@app.route("/delete_message", methods=["GET", "POST"])
@cross_origin()
def delete_message():
    if request.method == "POST":
        try:
            #GET INFO
            deletemessage_id = utils.delete_message(request)

            #CHECK VALIDATE INFOR SENT FROM USER
            if len(deletemessage_id) < 4:
                _, count_data = deletemessage_id
                if count_data == 0:
                    lost_field = "message_id"
                elif count_data == 1:
                    lost_field = "room_id"
                elif count_data == 2:
                    lost_field = "time_delete"
                elif count_data == 3:
                    lost_field = "status_delete"
                return jsonify(
                    {
                        "status": "error",
                        "message": "information not enough, recheck",
                        "lost": lost_field,
                    }
                )
            #SAVE INFORMATION TO SQL LITE.

            message_id = deletemessage_id[0]
            room_id = deletemessage_id[1]
            time_delete = deletemessage_id[2]
            status_delete = deletemessage_id[3]

            if time_delete != 0:
                time.sleep(time_delete)
                folder_face_path = "./datasqlite/room_active/" + "hello.db"
                conn = sqlite3.connect(folder_face_path)

                c = conn.cursor()
                c.execute(f"DELETE from information WHERE password = '{message_id}' ")
                conn.commit()

            # folder_face_path = "./datasqlite/room_active/" + "hello.db"
            # conn = sqlite3.connect(folder_face_path)
            #
            # c = conn.cursor()
            # c.execute(f"DELETE from information WHERE password = '{message_id}' ")
            #
            # conn.commit()

            return jsonify({"status": "success", "message": "successfully saved data"})
        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")
@app.route("/validateinfo", methods=["GET", "POST"])
@cross_origin()
def validate():
    if request.method == "POST":
        try:
            request_validate_signin = utils.validate(request)
            if len(request_validate_signin) < 2:
                _, count_data = request_validate_signin
                if count_data == 0:
                    lost_field = "username"
                elif count_data == 1:
                    lost_field = "password"
                return jsonify(
                    {
                        "status": "error",
                        "message": "information not enough, recheck",
                        "lost": lost_field,
                    }
                )
            username_validate = request_validate_signin[0]
            password_validate = request_validate_signin[1]
            folder_path = "./datasqlite/" + f'{username_validate}.db'
            if(os.path.isfile(folder_path)):
                conn = sqlite3.connect(folder_path)
                conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
                db = conn.cursor()

                rows = db.execute('''
                                SELECT * from information
                                ''').fetchall()

                conn.commit()
                json_data = [dict(ix) for ix in rows]

                return jsonify(json_data)
        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")


@app.route("/joinroom", methods=["GET", "POST"])
@cross_origin()
def join_room():
    if request.method == "POST":
        try:
            request_join_room = utils.join_room(request)
            if len(request_join_room) < 2:
                _, count_data = request_join_room
                if count_data == 0:
                    lost_field = "customer_id_username"
                elif count_data == 1:
                    lost_field = "user_send_id"
                return jsonify(
                {
                    "status": "error",
                    "message": "information not enough, recheck",
                    "lost": lost_field,
                }
            )
            customer_id_username = request_join_room[0]
            user_send_id = request_join_room[1]
            # print(request_join_room[0])
            # print(request_join_room[1])
            combine_username = str(customer_id_username) + "_" + str(user_send_id)

            folder_face_path = "./datasqlite/room_active/" + f'{combine_username}.db'
            conn = sqlite3.connect(folder_face_path)
            c = conn.cursor()
            c.execute(f"""CREATE TABLE information (
                        {customer_id_username} text,
                        {user_send_id} text,
                        DATACOMBO text,
                        FILETHINGS text,
                        GPS text)""")
            # c.execute(
            #     f"INSERT INTO information VALUES ('ronnie', 'ruby', 'meow', 'no', 'abc')")
            conn.commit()

            return jsonify({"status": "success", "message": "successfully saved data"})
        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")

@app.route("/joinroomdb", methods=["GET", "POST"])
@cross_origin()
def join_room_db():
    if request.method == "POST":
        try:
            request_joinroom_db = utils.join_room(request)
            if len(request_joinroom_db) < 2:
                _, count_data = request_joinroom_db
                if count_data == 0:
                    lost_field = "customer_id_username"
                elif count_data == 1:
                    lost_field = "user_send_id"
                return jsonify(
                {
                    "status": "error",
                    "message": "information not enough, recheck",
                    "lost": lost_field,
                }
            )
            customer_id_username = request_joinroom_db[0]
            user_send_id = request_joinroom_db[1]
            print(request_joinroom_db[0])
            print(request_joinroom_db)

            combine_username = customer_id_username + "_" + user_send_id
            folder_face_path = "./datasqlite/room_active/" + f'{combine_username}.db'

            conn = sqlite3.connect(folder_face_path)
            conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
            db = conn.cursor()

            rows = db.execute('''
                SELECT * from information
                ''').fetchall()

            conn.commit()
            json_data =[dict(ix) for ix in rows]

            return jsonify(json_data)

        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")
@app.route("/receivemessage", methods=["GET", "POST"])
@cross_origin()
def receive_message():
    if request.method == "POST":
        try:
            request_new_message = utils.send_message(request)
            if len(request_new_message) < 5:
                _, count_data = request_new_message
                if count_data == 0:
                    lost_field = "customer_send_info"
                elif count_data == 1:
                    lost_field = "user_receive_name"
                elif count_data == 2:
                    lost_field = "customer_send_info_text_image"
                elif count_data == 3:
                    lost_field = "customer_send_info_text_file"
                elif count_data == 4:
                    lost_field = "customer_send_info_text_gps"
                return jsonify(
                    {
                        "status": "error",
                        "message": "information not enough, recheck",
                        "lost": lost_field,
                    }
                )
            customer_send = request_new_message[0]
            user_receive = request_new_message[1]
            customer_send_info_text_image = request_new_message[2]
            customer_send_info_text_file = request_new_message[3]
            customer_send_info_text_gps = request_new_message[4]

            combine_username = customer_send + "_" + user_receive
            folder_face_path = "./datasqlite/room_active/" + f'{combine_username}.db'
            conn = sqlite3.connect(folder_face_path)
            c = conn.cursor()

            c.execute(
                f"INSERT INTO information VALUES ('{customer_send}', '{user_receive}', '{customer_send_info_text_image}','{customer_send_info_text_file}', '{customer_send_info_text_gps}')")
            conn.commit()

            return jsonify({"status": "success", "message": "successfully saved data"})
        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")


@app.route("/registeruser", methods=["GET", "POST"])
@cross_origin()
def receive_text():
    if request.method == "POST":
        try:
            #GET INFO
            request_register = utils.register_user(request)

            #CHECK VALIDATE INFOR SENT FROM USER
            if len(request_register) < 6:
                _, count_data = request_register
                if count_data == 0:
                    lost_field = "fullname"
                elif count_data == 1:
                    lost_field = "username"
                elif count_data == 2:
                    lost_field = "password"
                elif count_data == 3:
                    lost_field = "telephone"
                elif count_data == 4:
                    lost_field = "privateKeyFirst"
                elif count_data == 5:
                    lost_field = "avatar"
                return jsonify(
                    {
                        "status": "error",
                        "message": "information not enough, recheck",
                        "lost": lost_field,
                    }
                )
            #SAVE INFORMATION TO SQL SERVER.
            fullname = request_register[0]
            #print(fullname)
            username = request_register[1]
            password = request_register[2]
            telephone = request_register[3]
            privateKeyFirst = request_register[4]
            avatar = request_register[5]


            folder_face_path = "./datasqlite/" + f'{username}.db'
            # folder_face_path = "./datasqlite/room_active/" + "hello.db"
            conn = sqlite3.connect(folder_face_path)
            c = conn.cursor()
            c.execute("""CREATE TABLE information (
                        fullname text,
                        username text,
                        password text,
                        telephone text,
                        privateKeyFirst text,
                        avatar text)""")
            c.execute(f"INSERT INTO information VALUES ('{fullname}', '{username}', '{password}', '{telephone}', '{privateKeyFirst}', '{avatar}')")
            conn.commit()

            return jsonify({"status": "success", "message": "successfully saved data"})
        except Exception as e:
            print(f"Error:: {str(e)}")
            return jsonify("fail")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
