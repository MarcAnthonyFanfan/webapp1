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
            return response
        else:
            return render_template('index.html')

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
            cur1 = mysql.connection.cursor()
            cur1.execute("SELECT * FROM users WHERE username='%s'", [username])
            if cur1.rowcount == 0:
                cur2 = mysql.connection.cursor()
                cur2.execute("INSERT INTO users(username, password) VALUES ('%s', '%s')", (username, password))
                response = make_response(redirect('/dashboard'))
                response.set_cookie('username', username)
            else:
                response = make_response(redirect('/sign_up'))
                flash("Username already exists")
            return response

    @app.route('/log_in', methods=['GET', 'POST'])
    def log_in():
        return "TO DO: log_in page"

    return app