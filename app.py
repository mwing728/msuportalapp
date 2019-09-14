from flask import Flask, render_template, request, redirect, flash, url_for, session, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import loginApp as loginFunction
import registerApp as registerFunction
import questionsApp as questionsFunction
import teachersApp as teachersFunction
import datetime
from flask_socketio import SocketIO
app = Flask(__name__)
#config mysql
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-02.cleardb.net'
app.config['MYSQL_USER'] = 'b693543105bea1'
app.config['MYSQL_PASSWORD'] = 'e9b1bf91'
app.config['MYSQL_DB'] = 'heroku_b73dff108c0f588'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
socketio = SocketIO(app)
#init MySQL
mysql = MySQL(app)


#Question form class
class QuestionAnswerForm(Form):
	textBox = StringField('textBox', [validators.Length(min=1)])


#index route

@app.route('/', methods=['GET'])
def index():
	return loginFunction.login()

#home route

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

#Register Route

@app.route('/register', methods=['GET','POST'])
def register():
	return registerFunction.register()
@app.route('/login', methods=['GET', 'POST'])
def login():
	return loginFunction.login()

@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

@app.route('/questions', methods =['GET', 'POST'])

def questions():
	return questionsFunction.questions()

@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
	return teachersFunction.teachers()

@app.route('/users', methods=['GET', 'POST'])
def users():
	if request.method == "POST":
		app.logger.info(request.form['nameUser'])
		if 'deleteUser' in request.form:
			user = request.form['nameUser']
			cur = mysql.connection.cursor()
			result = cur.execute("DELETE FROM Registration WHERE Email = %s", (user,))

			mysql.connection.commit()

			cur.close()
			app.logger.info("You have successfully deleted a question")
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM Registration")
	data = cur.fetchall()
	if result > 0:
		return render_template('users.html', data = data)
	else:
		msg = "No Users are Registered"
		return render_template('users.html', msg=msg)
@app.route('/chat', methods = ['GET', 'POST'])
def chat():
	return render_template('chat.html')
def messageReceived(methods=['GET','POST']):
	print('message was received')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	app.logger.info('received my event: '+ str(json))
	socketio.emit('my response', json, callback=messageReceived)

#main method
if __name__ == "__main__":
	app.secret_key= "secretstuff"
	# app.run(debug=True)
	socketio.run(app, debug=True)