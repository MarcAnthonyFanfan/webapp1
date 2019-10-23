import os
import sys

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = '127.0.0.1'
    app.config['MYSQL_USER'] = 'flask'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'flaskapp'
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

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == "POST":
            details = request.form
            username = details['username']
            password = details['password']
            cur = mysql.connection.cursor()
            try:
                cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            mysql.connection.commit()
            cur.close()
            return 'success'
        return render_template('index.html')

    return app