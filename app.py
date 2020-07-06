from flask import Flask, render_template, session, redirect, url_for, request
from flask_pymongo import pymongo
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

client = pymongo.MongoClient('localhost', 27017)

db = client.test


@app.route("/")
def index():
    if "username" in session:
        db.posts.insert_one({"Name":"Serban"})
        return render_template("index.html", user=session["username"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"]=request.form["username"]
        session["password"]=request.form["password"]
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username", None)
    else:
        pass
    return redirect(url_for("login"))


if __name__ == '__main__':
    # Start the Flask web server
    app.run(host='0.0.0.0', debug=True,port=5000)