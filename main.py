from flask import Flask, request, render_template, redirect, url_for, session,flash
from markupsafe import escape
from flask_mail import Mail, Message
from config import configEmail
from time import time
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

@app.route('/Logout')
def Logout():
    session.pop('email' , None)
    return redirect(url_for("Login"))




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




if __name__ == "__main__":
    app.run(debug=True)
