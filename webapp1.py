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
            user_cookie = request.cookies.get('username')
            return "Hello " + user_cookie
        else:
            redirect('/sign_up')

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
            if cur.rowcount == 0:
                cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
                msg = "You were successfully logged in"
                response = make_response(redirect('/'))
                response.set_cookie('username', username)
            else:
                response = make_response(redirect('/sign_up'))
                msg = "Username already exists"
            flash(msg)
            return response

    return app