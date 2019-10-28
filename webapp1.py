import os
import sys
import hashlib

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

    @app.route('/', methods=['GET'])
    def index():
        if 'username' in request.cookies:
            response = make_response(redirect('/dashboard'))
        else:
            response = make_response(redirect('/log_in'))
        return response

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [request.cookies.get('username')])
        mysql.connection.commit()
        user = cur.fetchall()[0]
        cur.execute("SELECT requests.id, users.username, requests.type, requests.approved FROM requests INNER JOIN users ON requests.user_id=users.id")
        mysql.connection.commit()
        requests = cur.fetchall()
        if request.method == "GET":
            cur.close()
            return render_template('dashboard.html', user=user, requests=requests)
        else:
            details = request.form
            print(details, file=sys.stderr)
            approved_list = request.form.getlist("approved")
            if user[3]==True:
                i = 0
                for approval in approved_list:
                    if approval == '1':
                        cur.execute("UPDATE requests SET approved='1' where id=%s AND approved='0'", [requests[i][0]])
                        mysql.connection.commit()
                    i += 1
                response = make_response(redirect('/dashboard'))
            else:
                network_request = details['network_request']
                if network_request == '1':
                    cur.execute("INSERT INTO requests(user_id, type) VALUES (%s, %s)", (user[0], "Network"))
                    mysql.connection.commit()
                    response = make_response(redirect('/dashboard'))
            cur.close()
            return response


    @app.route('/sign_up', methods=['GET', 'POST'])
    def sign_up():
        if request.method == "GET":
            return render_template('sign_up.html')
        else:
            details = request.form
            email = details['email']
            username = details['username']
            password = details['password']
            confirm_password = details['confirm_password']
            agree = details['agree']
            if password != confirm_password:
                response = make_response(redirect('/sign_up'))
                flash("Password and password confirmation do not match")
            elif agree != '1':
                response = make_response(redirect('/sign_up'))
                flash("You must agree to the terms and conditions")
            else:
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM users WHERE username=%s", [username])
                mysql.connection.commit()
                if cur.rowcount == 0:
                    secure_password = hashlib.sha256((username.lower()+password).encode('utf-8')).hexdigest()[:32]
                    cur.execute("INSERT INTO users(email, username, password) VALUES (%s, %s, %s)", (email, username, secure_password))
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
            secure_password = hashlib.sha256(username.lower()+password.encode('utf-8')).hexdigest()[:32]
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", [username, secure_password])
            mysql.connection.commit()
            if cur.rowcount == 0:
                response = make_response(redirect('/log_in'))
                flash("Incorrect username/password combination")
            else:
                response = make_response(redirect('/dashboard'))
                response.set_cookie('username', username)
            cur.close()
            return response
    
    @app.route('/log_out', methods=['GET'])
    def log_out():
        response = make_response(redirect('/dashboard'))
        response.set_cookie('username', '', expires=0)
        return response

    return app