import os
import sys

from flask import Flask, render_template, request, flash, redirect, url_for, make_response
from flask_mysqldb import MySQL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'flask'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'flaskapp'
    app.secret_key = 'dev'
    mysql = MySQL(app)

    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)

    #if test_config is None:
    #    # load the instance config, if it exists, when not testing
    #    app.config.from_pyfile('config.py', silent=True)
    #else:
    #    # load the test config if passed in
    #    app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', methods=['GET'])
    def index():
        if 'username' in request.cookies:
            response = make_response(redirect('/dashboard'))
        else:
            response = make_response(redirect('/log_in'))
        return response

    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        if 'username' in request.cookies:
            return render_template('dashboard.html')
        else:
            response = make_response(redirect('/'))
            flash("You must be logged in to view the Dashboard")
            return response

    @app.route('/sign_up', methods=['GET', 'POST'])
    def sign_up():
        if request.method == "GET":
            return render_template('sign_up.html')
        else:
            details = request.form
            username = details['username']
            password = details['password']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s", [username])
            mysql.connection.commit()
            if cur.rowcount == 0:
                cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
                mysql.connection.commit()
                response = make_response(redirect('/dashboard'))
                response.set_cookie('username', username)
            else:
                response = make_response(redirect('/sign_up'))
                flash("Username already exists")
            cur.close()
            return response

    @app.route('/log_in', methods=['GET', 'POST'])
    def log_in():
        if request.method == "GET":
            return render_template('log_in.html')
        else:
            details = request.form
            username = details['username']
            password = details['password']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", [username, password])
            mysql.connection.commit()
            if cur.rowcount == 0:
                response = make_response(redirect('/log_in'))
                flash("Incorrect username/password combination")
            else:
                response = make_response(redirect('/dashboard'))
                response.set_cookie('username', username)
            cur.close()
            return response

    return app