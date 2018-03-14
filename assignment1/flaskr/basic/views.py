from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        code = models.validateUser(username, password)
        if code == 403:
            return "Invalid username or password", 403
        else:
            session['username'] = username
            return redirect(url_for("basic.users", account=username))

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        code = models.registerUser(username, password)
        if code == 400:
            return "Username already in use", 400
        elif code == 500:
            return "Errors, try later", 500
        elif code == 302:
            return redirect(url_for("basic.login"))

    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    if session.get('username') is not None:
        if(session.get('username') == account or account.lower() == "me"):
            return render_template("users.html", account= session.get('username'))

    return "Please login first", 403
