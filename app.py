from flask import Flask, redirect, render_template, request
from libs import helpers as do
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favorites", methods=["POST"])
def favorites():
    username = request.form.get("username")
    if not username: #or ["'", '"', ' ', '.'] in username:
        return render_template("failure.html", username=username)

    favorites = do.getLeagueMatesFavorites(do.getUserID(username))

    return render_template("table.html", favorites=favorites, username=username)
