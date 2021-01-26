from flask import Flask, request, render_template, redirect, url_for, session,flash
from markupsafe import escape
from flask_mail import Mail, Message
from config import configEmail
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

def initApp():
    return app

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
        for e in info:
            if email == e[0]:
                return "Email already exists please use another email", 10
        val = (email , password)
        query = "INSERT INTO users(Email,Password) VALUES(%s , %s)"
        if conn.executeQueryValNonData(query , val):
            return "Thank you for sign up" , 200
        else:
            return "Server error please try again", 200
    else:
        return render_template("Account/Register.html")

@app.route('/Logout')
def Logout():
    session.pop('email' , None)
    return redirect(url_for("Login"))




def sendEmail(subject , recipients, token):
    msg = Message(subject=subject , recipients=recipients)
    msg.html = '''
    <h1>Welcome</h1>
    <p>You have requested to registration for SOA account. Please click link bellow to confirm</p>
    <p>Link: </p>
    '''




if __name__ == "__main__":
    app.run(debug=True)
