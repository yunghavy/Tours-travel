import pymysql
from conda.gateways import connection
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_login import login_required, logout_user
from sqlalchemy.sql.functions import *

connection = pymysql.connect(host='localhost', user='root', password='', database='Travel')
print("Database connection successful")

# def check_user():
#     if 'email' in session:
#         return True
#     else:
#         return False


# start
app = Flask(__name__)
app.secret_key = "IloveProgramming"


@app.route('/')
def index():
    # login = False
    # if 'username' in session:
    #     login = True
    if 'key' in session:

        return render_template('index.html', login=login)
    else:
        return redirect('/login')


@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        connection = pymysql.connect(host='localhost', user='root', password='', database='Travel')
        print("Database connection successful")
        cursor = connection.cursor()
        sql = 'INSERT INTO users (username, email, password) VALUES (%s,%s,%s)'

        cursor.execute(sql, (user_name, user_email, user_password))
        connection.commit()
        return render_template('login.html', message="Registered successfully")
    else:
        return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        user_email = request.form['email']
        user_password = request.form['password']
        connection = pymysql.connect(host='localhost', user='root', password='', database='Travel')
        print("Database connection successful")
        cursor = connection.cursor()
        sql = 'SELECT * FROM users WHERE email =%s AND password =%s'

        cursor.execute(sql, (user_email, user_password))

        if cursor.rowcount == 0:
            return render_template('login.html', error="Invalid Credentials, Try Again")
        elif cursor.rowcount == 1:
            row = cursor.fetchone()
            session['logged_in'] = True
            session['username'] = row[1]
            session['email'] = row[2]  # user_email
            session['user_id'] = row[0]
            session['key'] = row[1]
            return redirect('/')
        else:
            return render_template('login.html', error="Something wrong with credentials")
    else:
        return render_template('login.html')


@app.route('/booking', methods=['POST', 'GET'])
def booking():
    if 'key' in session:
        if request.method == 'POST':
            email = request.form['email']
            phone = request.form['phone']
            destination_to = request.form['destTo']
            destination_from = request.form['destFrom']
            booking_time = request.form['time']
            booking_date = request.form['date']
            connection = pymysql.connect(host='localhost', user='root', password='', database='Travel')
            print("Database connection successful")
            cursor = connection.cursor()
            sql = 'INSERT INTO book (email, phone, destination_to, destination_from, booking_time, booking_date) ' \
                  'VALUES (%s,%s,' \
                  '%s,%s,%s,%s) '
            cursor.execute(sql, (email, phone, destination_to, destination_from, booking_time, booking_date))
            connection.commit()
            return render_template('index.html', message="Trip booked successfully")
        else:
            return render_template('booking.html')
    else:
        return redirect('/login')


@app.route('/bookings')
def check_booking():
    cursor = connection.cursor()
    sql = 'SELECT * FROM book'
    cursor.execute(sql)
    book = cursor.fetchall()
    return render_template('bookings.html', book=book)


@app.route('/users')
def check_users():
    cursor = connection.cursor()
    sql = 'SELECT * FROM users'
    cursor.execute(sql)
    users = cursor.fetchall()
    return render_template('users.html', users=users)


# Admin Login

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


app.run(debug=True)
