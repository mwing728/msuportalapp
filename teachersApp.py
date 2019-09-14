from flask import Flask, render_template, request, redirect, flash, url_for, session, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import datetime
from flask_socketio import SocketIO
app = Flask(__name__)

#config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'MSUPortal'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
socketio = SocketIO(app)
#init MySQL
mysql = MySQL(app)

def teachers():
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM Teachers")
	data = cur.fetchall()

	if result > 0:
		return render_template('teachers.html', data = data)
	else:
		msg = "No Teachers Available"
		return render_template('teachers.html', msg=msg)
	cur.close()