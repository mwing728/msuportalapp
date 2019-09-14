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

def questions():
	if request.method == "POST":
		if 'Submit_Question' in request.form:
			#grabbing user question from form
			userQuestion = request.form['questionInp']
			today = datetime.date.today()
			#making a cursor for sql query
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO Questions(question, Email, Date) VALUES(%s, %s, %s)", (userQuestion, session['email'], today))

			#commit to db
			mysql.connection.commit()

			#close connection
			cur.close()
			app.logger.info("You have successfully entered in a Question")
		else:
			app.logger.info("Something went wrong with the sql")
	if request.method == "POST":
		if 'Submit_Answer' in request.form:
			textAnswer = request.form['txt']
			ID = request.form['questionID']
			cur = mysql.connection.cursor()

			result = cur.execute("UPDATE Questions SET answer = %s WHERE ID = %s", (textAnswer, ID))

			mysql.connection.commit()

			cur.close()
			app.logger.info("You have successfully entered in a Answer")
	if request.method == "POST":
		if 'Delete_Question' in request.form:
			ID = request.form['questionIDDelete']
			cur = mysql.connection.cursor()
			app.logger.info(ID)
			result = cur.execute("DELETE FROM Questions WHERE ID = %s", (ID,))

			mysql.connection.commit()

			cur.close()
			app.logger.info("You have successfully deleted a question")
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM Questions ORDER BY ID DESC")
	questions = cur.fetchall()

	if result > 0:
		return render_template('questions.html', questions=questions)
	else:
		msg = "No Questions found"
		return render_template('questions.html', msg=msg)
	cur.close()