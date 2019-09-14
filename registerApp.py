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

class RegisterForm(Form):
	FirstName = StringField('FirstName', [validators.Length(min=1, max = 50)])
	LastName = StringField('LastName', [validators.Length(min=1, max=50)])
	Email = StringField('email', [validators.Length(min=1, max=50)])
	password = PasswordField('Password', 
	[
		validators.DataRequired(), 
		validators.EqualTo('confirm', message = 'Passwords do not match')
	
	])
	confirm = PasswordField('passwordAgain')

def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		FirstName = form.FirstName.data
		LastName = form.LastName.data
		email = form.Email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#create cursor
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO Registration(FirstName, LastName, Email, Password, EmpType) VALUES(%s, %s, %s, %s, 'C')", (FirstName, LastName, email, password))

		#commit to DB
		mysql.connection.commit()

		cur.execute("INSERT INTO Login(Email, Password, EmpType) VALUES(%s, %s, 'C')", (email, password))

		#commit to DB
		mysql.connection.commit()

		#close Connection

		cur.close()

		flash('You are now registered and can log in', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)