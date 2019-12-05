import os
import sys
import hashlib
import random

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
    
    @app.route('/hello', methods=['GET'])
    def hello():
        return "Hello"

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [request.cookies.get('username')])
        mysql.connection.commit()
        user = cur.fetchall()[0]
        if user[4]==True:
            cur.execute("SELECT requests.id, users.username, requests.type, requests.approved FROM requests INNER JOIN users ON requests.user_id=users.id")
        else:
            cur.execute("SELECT requests.id, users.username, requests.type, requests.approved FROM requests INNER JOIN users ON requests.user_id=users.id WHERE requests.user_id=%s", [user[0]])
        mysql.connection.commit()
        requests = cur.fetchall()
        if request.method == "GET":
            cur.close()
            return render_template('dashboard.html', user=user, requests=requests)
        else:
            details = request.form
            approved_list = request.form.getlist("approved")
            if user[4]==True:
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

    @app.route('/profile', methods=['GET'])
    def profile():
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [request.cookies.get('username')])
        mysql.connection.commit()
        user = cur.fetchall()[0]
        cur.close()
        return render_template('profile.html', user=user)

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
                cur.execute("SELECT * FROM users WHERE email=%s OR username=%s", [email, username])
                mysql.connection.commit()
                if cur.rowcount == 0:
                    secure_password = hashlib.sha256((username.lower()+password).encode('utf-8')).hexdigest()[:32]
                    cur.execute("INSERT INTO users(email, username, password) VALUES (%s, %s, %s)", (email, username, secure_password))
                    mysql.connection.commit()
                    response = make_response(redirect('/dashboard'))
                    response.set_cookie('username', username)
                else:
                    response = make_response(redirect('/sign_up'))
                    flash("Username or Email already exists")
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
            secure_password = hashlib.sha256((username.lower()+password).encode('utf-8')).hexdigest()[:32]
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
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        response = make_response(redirect('/dashboard'))
        response.set_cookie('username', '', expires=0)
        return response
    
    @app.route('/delete_account', methods=['GET'])
    def delete_account():
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [request.cookies.get('username')])
        mysql.connection.commit()
        user = cur.fetchall()[0]
        cur.execute("DELETE FROM users WHERE id=%s", [user[0]])
        mysql.connection.commit()
        cur.execute("DELETE FROM requests WHERE user_id=%s", [user[0]])
        mysql.connection.commit()
        cur.close()
        response = make_response(redirect('/dashboard'))
        response.set_cookie('username', '', expires=0)
        return response

    @app.route('/reset_password', methods=['GET', 'POST'])
    def reset_password():
        if request.method == "GET":
            return render_template('reset_password.html')
        else:
            details = request.form
            email = details['email']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email=%s", [email])
            mysql.connection.commit()
            if cur.rowcount == 0:
                response = make_response(redirect('/reset_password'))
                cur.close()
                flash("No account with such email: " + email)
                return response
            else:
                user = cur.fetchall()[0]
                new_password = new_random_password()
                secure_password = hashlib.sha256((user[2].lower()+new_password).encode('utf-8')).hexdigest()[:32]
                cur.execute("UPDATE users SET password=%s WHERE email=%s AND username=%s", (secure_password, email, user[2]))
                mysql.connection.commit()
                cur.close()
                print(("Password reset for user: " + user[2] + " temporary password: " + new_password), file=sys.stderr)
                if os.environ.get('FLASK_ENV') is not None:
                    if os.environ['FLASK_ENV'] == 'development':
                        return render_template('reset_password_email.html', user=user, new_password=new_password)
                response = make_response(redirect('/log_in'))
                flash("A password reset link has been emailed to: " + email)
                return response
    
    @app.route('/change_password', methods=['GET', 'POST'])
    def change_password():
        if 'username' not in request.cookies:
            response = make_response(redirect('/'))
            return response
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", [request.cookies.get('username')])
        mysql.connection.commit()
        user = cur.fetchall()[0]
        if request.method == "GET":
            cur.close()
            return render_template('change_password.html', user=user)
        else:
            details = request.form
            old_password = details['old_password']
            secure_old_password = hashlib.sha256((user[2].lower()+old_password).encode('utf-8')).hexdigest()[:32]
            new_password = details['new_password']
            confirm_new_password = details['confirm_new_password']
            secure_new_password = hashlib.sha256((user[2].lower()+new_password).encode('utf-8')).hexdigest()[:32]
            if secure_old_password != user[3]:
                response = make_response(redirect('/change_password'))
                flash("Incorrect current password")
            elif new_password != confirm_new_password:
                response = make_response(redirect('/change_password'))
                flash("New password and confirmation do not match")
            else:
                cur.execute("UPDATE users SET password=%s WHERE email=%s AND username=%s", (secure_new_password, user[1], user[2]))
                mysql.connection.commit()
                response = make_response(redirect('/profile'))
                flash("Your password has been changed")
            cur.close()
            return response
    
    def new_random_password(length=10):
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()<>'
        return ''.join((random.choice(alphabet) for i in range(length)))

    return app