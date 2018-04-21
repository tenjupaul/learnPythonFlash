import os
import pymysql

from flask import Flask, request, render_template, redirect, url_for, flash, make_response, session
app = Flask(__name__)

#import logging
#from logging.handlers import RotatingFileHandler 

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form.get('username'), request.form.get('password')):
            flash("Succesfully logged in")
            session['username'] = request.form.get('username')
            return redirect(url_for('welcome'))
        else:
            error = "Incorrect username and password"
            #app.logger.warning('Incorrect Username or Password for user (%s)', request.form.get('username'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('login'))

def valid_login(username, password):
    #mysql
    MYSQL_DATABASE_HOST = 'sql3.freesqldatabase.com'
    MYSQL_DATABASE_USER = 'sql3233839'
    MYSQL_DATABASE_PASSWORD = 'REEwreYmFL'
    MYSQL_DATABASE_DB = 'sql3233839'
    MYSQL_DATABASE_PORT = 3306

    conn = pymysql.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        passwd=MYSQL_DATABASE_PASSWORD,
        db=MYSQL_DATABASE_DB,
        port=MYSQL_DATABASE_PORT
        )
    cursor = conn.cursor()
    cursor.execute("SELECT * from user WHERE username='%s' AND password='%s'" %(username,password))
    data = cursor.fetchone()

    if data:
        return True
    else:
        return False

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'SuperSecretKey'

    #logging
    #handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    #handler.setLevel(logging.INFO)
    #app.logger.addHandler(handler)

    app.run(app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8080))))
