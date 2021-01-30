from flask import Flask, request, render_template, redirect, url_for, session,flash
from markupsafe import escape
from flask_mail import Mail, Message
from config import configEmail
from time import time
import random as rd
import os
import hashlib
import connection as conn
app = Flask(__name__, template_folder="Views")
app.secret_key = b'HieuPham-518H0501'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = configEmail["Username"]
app.config['MAIL_PASSWORD'] = configEmail["Password"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'Admin'
mail = Mail(app)
UPLOAD_FOLDER = 'static/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        password = hashlib.sha512(str.encode(data['password'])).hexdigest()
        val = (email , password)
        query = "SELECT * FROM users WHERE Email = %s AND Password = %s"
        info = conn.executeQueryValData(query, val)
        if len(info) == 1:
            session['email'] = email
            return url_for("Home")
        else:
            return "Invalid email or password please try again", 10
    else:
        if 'email' in session:
            return redirect(url_for('Home'))
        return render_template("Account/Login.html")


@app.route('/Home')
def Home():
    if 'email' in session:
        flash('You logged in as %s' % escape(session['email']))
        return render_template("Home/index.html")
    else:
        return redirect(url_for('Login'))


@app.route('/Register', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':
        data = request.json
        query = "SELECT Email FROM users"
        info = conn.executeQueryData(query)
        email = data['email']
        password = hashlib.sha512(str.encode(data['password'])).hexdigest()
        token = hashlib.sha512(str.encode(email + str(time()))).hexdigest()
        departTime = int(time())
        recipients = [email]
        for e in info:
            if email == e[0]:
                return "Email already exists please use another email", 10
        val = (token, departTime, email, password)
        query = "INSERT INTO verifyaccount(Token,DepartTime,Email,Password) VALUES(%s , %s, %s, %s)"
        if conn.executeQueryValNonData(query , val):
            sendEmail("Sign Up" , recipients , token)
            return "Please check your email to complete registration" , 200
        else:
            return "Server error please try again", 200
    else:
        return render_template("Account/Register.html")

@app.route('/ConfirmSignUp/<token>')
def confirmSignUp(token):
    val = (token)
    query = "SELECT * FROM verifyaccount WHERE Token = %s"
    info = conn.executeQueryValData(query, val)
    if len(info) <= 0:
        return "Not Found" , 404
    currentTime = time()
    departTime = info[0][2]
    if currentTime - departTime > 600:
        query = "DELETE FROM verifyaccount WHERE Token = %s"
        conn.executeQueryValNonData(query , val)
        return "<h1>Sorry email expired, please try again</h1>"
    else:
        query = "DELETE FROM verifyaccount WHERE Token = %s"
        conn.executeQueryValNonData(query , val)
        email = info[0][3]
        password = info[0][4]
        query = "INSERT INTO users(Email,Password) VALUES(%s,%s)"
        val = (email , password)
        if conn.executeQueryValNonData(query,val):
            return '''
            <h1>Thank you for sign up</h1>
            <a href="http://127.0.0.1:5000/">Login</a>
            '''
    return "Server error please try again"

@app.route('/RequestOTP' , methods=['POST' , 'GET'])
def RequestOTP():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        val = (email)
        query = "SELECT * FROM users WHERE Email = %s"
        info = conn.executeQueryValData(query, val)
        if len(info) == 1:
            otp = generateOTP()
            sendOTP("OTP" , [email] , otp)
            query = "INSERT INTO otp(Code, Email,DepartTime) VALUES(%s,%s,%s)"
            val = (otp,email,int(time()))
            conn.executeQueryValNonData(query,val)
            return render_template("Account/ConfirmOTP.html" , msg="Please check your email to get OTP code" , email=email)
        else:
            error = "Email does not exists please try again"
    return render_template("Account/LoginWithOTP.html" , error=error)

@app.route('/LoginOTP', methods=['POST'])
def LoginOTP():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        otp = data['otp']
        query = "SELECT * FROM otp WHERE Code = %s AND Email = %s"
        val = (otp , email)
        info = conn.executeQueryValData(query, val)
        if len(info) == 1:
            currentTime = int(time())
            departTime = info[0][3]
            if currentTime - departTime > 60:
                query = "DELETE FROM otp WHERE Code = %s AND Email = %s"
                val = (otp,email)
                conn.executeQueryValNonData(query , val)
                return "Sorry OTP code expired, please try again", 10
            else:
                session['email'] = email
                query = "DELETE FROM otp WHERE Email = %s"
                val = (email)
                conn.executeQueryValNonData(query , val)
                return url_for("Home")
        else:
            return "Invalid OTP code please try again",10
    return "File Not Found" , 404

@app.route('/Uploads' , methods=['POST' , 'GET'])
def Uploads():
    if request.method == 'POST':
        email = session['email']
        path = app.config['UPLOAD_FOLDER'] + '/' + email
        file = request.files['fileUpload']
        filename = file.filename
        if not os.path.exists(path):
            os.makedirs(path)
        if filename == '':
            return "No file attached"
        else:
            fileN = str(time()) + filename
            file.save(os.path.join(path, fileN))
            query = "SELECT UserID FROM users WHERE Email = %s"
            val = (email)
            info = conn.executeQueryValData(query , val)
            UserID = info[0][0]
            query = "INSERT INTO uploads(Path , FileName, UserID) VALUES(%s, %s, %s)"
            val = ( path + '/' + fileN , filename, UserID)
            conn.executeQueryValNonData(query,val)
            return "Success"
    else:
        if 'email' in session:
            email = session['email']
            query = "SELECT UserID FROM users WHERE Email = %s"
            val = (email)
            info = conn.executeQueryValData(query , val)
            UserID = info[0][0]
            query = "SELECT * FROM uploads WHERE UserID = %s"
            val = (UserID)
            info = conn.executeQueryValData(query , val)
            return render_template('Home/Uploads.html' , data=info)


@app.route('/Logout')
def Logout():
    session.pop('email' , None)
    return redirect(url_for("Login"))



def sendOTP(subject , recipients, OTP):
    msg = Message(subject=subject , recipients=recipients)
    body = '''
    <h1>Hello</h1>
    <p>{} is the otp authentication code for your login. </p>
    <p style="color:red">* This code is valid only for 1 minute.</p>
    '''
    msg.html = body.format(OTP)
    mail.send(msg)


def sendEmail(subject , recipients, token):
    msg = Message(subject=subject , recipients=recipients)
    host = "http://127.0.0.1:5000/ConfirmSignUp/{}"
    link = host.format(token)
    body = '''
    <h1>Welcome</h1>
    <p>You have requested to registration for SOA account. Please click link bellow to confirm</p>
    <p>Link: {}</p>
    <p style="color:red">* This email is valid only for 10 minutes</p>
    <p>if it's not you, please ignore this email</p>
    '''
    msg.html = body.format(link)
    mail.send(msg)



def generateOTP():
    OTP = ""
    for i in range(0,6):
        OTP += str(rd.randint(0,9))
    return OTP

if __name__ == "__main__":
    app.run(debug=True)
