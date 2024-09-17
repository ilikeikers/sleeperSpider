from flask import Flask, redirect, render_template, request
from libs import helpers as do
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/favorites", methods=["POST"])
def favorites():
    username = request.form.get("username")
    if not username or not username.isalnum():
        return render_template("failure.html", username=username)

    favorites = do.getLeagueMatesFavorites(do.getUserID(username))

    return render_template("table.html", favorites=favorites, username=username)
