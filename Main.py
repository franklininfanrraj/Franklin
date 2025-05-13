from flask import Flask, render_template, flash, request, session, send_file
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import datetime
import mysql.connector
import sys

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/Search")
def Search():
    return render_template('Search.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/SetLimit")
def SetLimit():
    user = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM limtb where  username ='" + user + "' ")
    data = cur.fetchall()

    return render_template('Limit.html', data=data)


@app.route("/MonthReport")
def MonthReport():
    return render_template('MonthReport.html')


@app.route("/Report")
def Report():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM expensetb ")
    data = cur.fetchall()

    return render_template('Report.html', data=data)


@app.route("/UserHome")
def UserHome():
    user = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + user + "'")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


        else:
            print(data[0])
            session['uid'] = data[0]
            session['mobile'] = data[4]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/ForgetPassword")
def ForgetPassword():
    return render_template('Fpassword.html')


@app.route("/getotp", methods=['GET', 'POST'])
def getotp():
    if request.method == 'POST':
        username = request.form['uname']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)


        else:

            session['uid'] = data[0]
            session['mobile'] = data[4]
            import random
            n = random.randint(1111, 9999)
            session['otp'] = n
            sendmsg(session['mobile'], "OTP : " + str(n))

            return render_template('Forgerpass.html')


@app.route("/fffpass", methods=['GET', 'POST'])
def fffpass():
    if request.method == 'POST':

        password = request.form['password']
        cpassword = request.form['cpassword']
        otp = request.form['otp']

        if str(otp) == str(session['otp']):
            if password == cpassword:

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
                cursor = conn.cursor()
                cursor.execute(
                    "update   regtb  set Password='" + password + "'where username='" + session['uname'] + "'")
                conn.commit()
                conn.close()
                alert = 'Password Reset!'
                return render_template('goback.html', data=alert)


            else:
                alert = 'Password  retype Password Incorrect!'
                return render_template('NewUser.html', data=alert)
        else:
            alert = 'Otp Incorrect..!'
            return render_template('goback.html',data=alert)


@app.route("/UReport")
def UReport():
    name1 = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')

    cur = conn.cursor()
    cur.execute("SELECT * FROM expensetb where username='" + name1 + "' ")
    data = cur.fetchall()
    return render_template('UReport.html', data=data)


@app.route("/dsearch", methods=['GET', 'POST'])
def dsearch():
    if request.method == 'POST':
        import cv2
        import datetime

        name1 = session['uname']
        type = request.form['c1']
        dat = request.form['t1']
        amt = request.form['t2']
        info = request.form['t3']

        file = request.files['fileupload']
        file.save('static/upload/' + file.filename)
        date_object = datetime.datetime.strptime(dat, '%Y-%m-%d').date()

        mon = date_object.strftime("%m")
        yea = date_object.strftime("%Y")
        print(mon)
        print(yea)

        global lim1
        global lim2

        lim1 = 0
        lim2 = 0

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * from limtb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Please Set Expense Limit'
            return render_template('goback.html', data=alert)


        else:

            lim1 = data[4]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT sum(Amount) as amt  from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "' ")
        data = cursor.fetchone()
        if data is None:
            lim2 = float(0.00)

            # alert = 'Please Set Expense Limit'
            # return render_template('goback.html', data=alert)


        else:

            lim2 = data[0]

        print(lim1)

        if lim2 is None:  # Checking if the variable is None

            lim2 = 0.00
        else:
            print("Not None")

        lim2 = float(lim2) + float(amt)

        if float(lim2) <= float(lim1):

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expensetb VALUES ('','" + name1 + "','" + type + "','" + dat + "','" + amt + "','" + info + "','" + file.filename + "','" +
                date_object.strftime("%m") + "','" + date_object.strftime("%Y") + "')")
            conn.commit()
            conn.close()

            alert = 'New Expense Info Saved'
            flash('New Expense Info Saved')

            return render_template('Search.html', result=amt)
        else:
            alert = 'Limit Above  Expense'
            msg = "Limit Amt:" + str(lim1) + " Above" + str(lim2)
            sendmsg(session['mobile'], msg);
            flash('Limit Above  Expense' + session['mobile'])

            return render_template('Search.html', result=amt)


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


@app.route("/setlimit", methods=['GET', 'POST'])
def setlimit():
    if request.method == 'POST':

        name1 = session['uname']
        mon = request.form['mon']
        yea = request.form['yea']
        amt = request.form['t2']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from limtb where username='" + name1 + "' and mon='" + mon + "' and yea='" + yea + "'")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO limtb VALUES ('','" + name1 + "','" + mon + "','" + yea + "','" + amt + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM limtb where  username ='" + name1 + "' ")
            data = cur.fetchall()

            return render_template('Limit.html', data=data)



        else:

            alert = 'Already Set  Expense limit Remove And Set New!'
            return render_template('goback.html', data=alert)


@app.route("/remove")
def remove():
    name1 = session['uname']

    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    cursor = conn.cursor()
    cursor.execute("delete from limtb  where Id='" + did + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM limtb where  username ='" + name1 + "' ")
    data = cur.fetchall()

    return render_template('Limit.html', data=data)


@app.route("/remove1")
def remove1():
    name1 = session['uname']

    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    cursor = conn.cursor()
    cursor.execute("delete from expensetb  where Id='" + did + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM expensetb where  username ='" + name1 + "' ")
    data = cur.fetchall()
    return render_template('UReport.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        pnumber = request.form['phone']
        address = request.form['address']

        uname = request.form['email']
        password = request.form['psw']
        cpsw = request.form['psw1']

        if password == cpsw:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from limtb where username='" + uname + "' ")
            data = cursor.fetchone()
            if data is None:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + email + "','" + password + "')")
                conn.commit()
                conn.close()
                # return 'file register successfully'
                return render_template('UserLogin.html')
            else:
                alert = 'Please Change  Email!'
                return render_template('NewUser.html', data=alert)


        else:
            alert = 'Password  retype Password Incorrect!'
            return render_template('NewUser.html', data=alert)


@app.route("/msearch", methods=['GET', 'POST'])
def msearch():
    if request.method == 'POST':
        if request.form["submit"] == "Search":

            mon = request.form['mon']
            yea = request.form['yea']
            uname = session['uname']

            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')

            mycursor = conn.cursor()
            mycursor.execute(
                "select Type, sum(Amount) as MSales from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + uname + "' group by Type ")
            result = mycursor.fetchall

            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in mycursor:
                Month.append(i[0])
                MSales.append(i[1])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Monthly Expenses")
            import random

            n = random.randint(1111, 9999)

            plt.savefig('static/plott/' + str(n) + '.jpg')

            iimg = 'static/plott/' + str(n) + '.jpg'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('MonthReport.html', data=data, dataimg=iimg)

        elif request.form["submit"] == "DSearch":
            d1 = request.form['d1']
            d2 = request.form['d2']
            uname = session['uname']

            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')

            mycursor = conn.cursor()
            mycursor.execute(
                "select Type, sum(Amount) as MSales,date from expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' group by Type ")
            result = mycursor.fetchall

            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in mycursor:
                Month.append(i[0])
                MSales.append(i[1])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Date To Date  Expenses")
            import random

            n = random.randint(1111, 9999)

            plt.savefig('static/plott/' + str(n) + '.jpg')

            iimg = 'static/plott/' + str(n) + '.jpg'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2Expensespydb')
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('MonthReport.html', data=data, dataimg=iimg)

    return render_template('goback.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
