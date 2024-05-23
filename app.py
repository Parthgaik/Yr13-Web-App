from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", title="Home" )


@app.route("/allcards")
def allcards():
    return render_template("allcards.html")


@app.route("/arenas")
def arenas():
    return render_template("arenas.html")


@app.route("/cardtype")
def cardtype():
    return render_template("cardtype.html")


if __name__ == "__main__":
    app.run(debug=True)
