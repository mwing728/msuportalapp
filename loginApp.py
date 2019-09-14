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

def login():
	if request.method == 'POST':
		#Get form fields
		email = request.form['email']
		password_candidate = request.form['password']

		#Create Cursor
		cur = mysql.connection.cursor()

		#Get user by email

		result = cur.execute("SELECT * FROM Login WHERE Email = %s", [email])

		if result > 0:
			#Get stored hash
			data = cur.fetchone()
			password = data['Password']
			EmpType = data['EmpType']

			#compare passwords
			if sha256_crypt.verify(password_candidate, password):
				#password passed
				app.logger.info('PASSWORD MATCHED')
				session['logged_in'] = True
				session['email'] = email
				session['emptype'] = EmpType

				flash('You are now logged in', 'success')
				return redirect(url_for('home'))
			else:
				error = "Invalid Login"
				return render_template('login.html', error=error)

			#connection close
			cur.close()
		else:
			error = "Username not found"
			return render_template('login.html', error=error)
	return render_template('login.html')