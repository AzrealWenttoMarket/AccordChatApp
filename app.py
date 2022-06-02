#Imports
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from werkzeug.security import check_password_hash, generate_password_hash

#importing SQLITE3 for database
import sqlite3
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
Socketio = SocketIO(app)

# App Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if the form is valid

            if not request.form.get("email") or not request.form.get("password") or not request.form.get("confirmation"):
                return "please fill out all fields"

            if request.form.get("password") != request.form.get("confirmation"):
                return "password confirmation doesn't match password"

            # check if email exist in the database
            exist = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()

            if len(exist) != 0:
                return "user already registered"

            # hash the password
            pwhash = generate_password_hash(request.form.get("password"), method="pbkdf2:sha256", salt_length=8)

            # insert the row
            c.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email": request.form.get("email"), "password": pwhash})
            conn.commit()

            # return success
            return "registered successfully!"
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # check the form is valid
        if not request.form.get("email") or not request.form.get("password"):
            return "please fill out all required fields"

        # check if email exist in the database
        user = c.execute("SELECT * FROM users WHERE email=:email", {"email": request.form.get("email")}).fetchall()

        if len(user) != 1:
            return "you didn't register"

        # check the password is same to password hash
        # this is using tuple checking the second column where the password field is.
        pwhash = user[0][1]
        if check_password_hash(pwhash, request.form.get("password")) == False:
            return "wrong password"

        # login the user using session
        session["user_id"] = user[0][0]

        # return success
        return redirect("/dashboard")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Event Listeners

@Socketio.on("broadcast message")
def message_display(data):
    #call this event in the client side and display the console.log data.message
    emit("show message", {"message": data["message"]},
    broadcast=True)

if __name__ == '__main__':
    Socketio.run(app, host="0.0.0.0", port=2000, debug=True)
