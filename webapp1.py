import os

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'mysql'
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
            firstName = details['fname']
            lastName = details['lname']
            cur = mysql.connection.cursor()
            #cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
            cur.execute("SHOW DATABASES")
            mysql.connection.commit()
            cur.close()
            return 'success'
        return render_template('templates/index.html')

    return app