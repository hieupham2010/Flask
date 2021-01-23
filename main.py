from flask import Flask, request , render_template , redirect, url_for
app = Flask(__name__ , template_folder="Views")


@app.route('/', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        email = "admin@gmail.com"
        password = "Admin@123"
        data = request.json
        if data['email'] == email and data['password'] == password :
            return url_for("Home") , 200
        else :
            return "Invalid email or password please try again" , 401
    else:
        return render_template("Account/Login.html")


@app.route('/Home')
def Home():
    return render_template("Home/index.html")

@app.route('/Register')
def Register():
    return render_template("Account/Register.html")

if __name__ == "__main__":
    app.run(debug=True)