from flask import Flask, request, render_template, redirect, url_for
import connection as conn
app = Flask(__name__, template_folder="Views")


@app.route('/', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = "admin@gmail.com"
        password = "Admin@123"
        data = request.json
        if data['email'] == email and data['password'] == password:
            return url_for("Home"), 200
        else:
            return "Invalid email or password please try again", 10
    else:
        return render_template("Account/Login.html")


@app.route('/Home')
def Home():
    return render_template("Home/index.html")


@app.route('/Register', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':
        data = request.json
        query = "SELECT Email FROM users"
        info = conn.executeQueryData(query)
        for e in info:
            if data['email'] == e[0]:
                return "Email already exists please use another email", 10
        val = (data['email'] , data['password'])
        query = "INSERT INTO users(Email,Password) VALUES(%s , %s)"
        if conn.executeQueryValNonData(query , val):
            return "Thank you for sign up" , 200
        else:
            return "Server error please try again", 200

    else:
        return render_template("Account/Register.html")


if __name__ == "__main__":
    app.run(debug=True)
