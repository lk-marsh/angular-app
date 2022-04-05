from venv import create

from app import app

import sqlite3
from sqlite3 import Error

from flask import jsonify
from flask import flash, request

db_file = "./db.db"

def generate_password_hash(pw):
    return pw		

def create_table():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS `tbl_user` (
        "user_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        `user_name` varchar(45) DEFAULT NULL,
        `user_email` varchar(45) DEFAULT NULL,
        `user_password` varchar(255) DEFAULT NULL
        );""")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
create_table()

@app.route('/add', methods=['POST'])
def add_user():
	conn = None
	cursor = None
	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']
		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES('{}', '{}', '{}')".format(_name, _email, _hashed_password)
			conn = sqlite3.connect(db_file)
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/users')
def users():
	conn = None
	cursor = None
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	conn = None
	cursor = None
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		cursor.execute( "SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user WHERE user_id={}".format(id) )
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['PUT'])
def update_user():
	conn = None
	cursor = None
	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']		
		# validate the received values
		if _name and _email and _password and _id and request.method == 'PUT':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = """UPDATE tbl_user SET user_name="{}", user_email="{}",user_password="{}" WHERE user_id={} """.format(_name, _email, _hashed_password, _id)
			conn = sqlite3.connect(db_file)
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	conn = None
	cursor = None
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_user WHERE user_id={}".format(id))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		
if __name__ == "__main__":
    app.run()