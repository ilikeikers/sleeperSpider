from flask import Flask, redirect, render_template, request
from libs import helpers as do
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    print("test")
    return render_template("index.html")

@app.route("/favorites", methods=["POST"])
def favorites():
    username = request.form.get("username")
    print("TEST")
    print(username)
    print(username.isalnum())
    #if not username: #or ["'", '"', ' ', '.'] in username:
    if not username.isalnum() or not username:
        return render_template("failure.html", username=username)

    favorites = do.getLeagueMatesFavorites(do.getUserID(username))

    return render_template("table.html", favorites=favorites, username=username)
