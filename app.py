from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def connect_database(statement, id=None):
    conn = sqlite3.connect("Yr13ClashRoyaleDB.db")
    cursor = conn.cursor()
    if id is not None:
        cursor.execute(statement, id)
    else:
        cursor.execute(statement)
    results = cursor.fetchall()
    conn.close()
    return results







@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/allcards")
def allcards():
    allcards = connect_database("SELECT id, name, Image FROM Cards")
    print(allcards, allcards[0])
    return render_template("allcards.html", title="All Cards", cards=allcards)

@app.route("/card")
def card():
    card = connect_database("SELECT id, name, Image FROM Cards")
    print(card, card[0])
    return render_template("card.html", title="{card[1]}", card=card)


@app.route("/arenas")
def arenas():
    return render_template("arenas.html")


@app.route("/cardtype")
def cardtype():
    return render_template("cardtype.html")


if __name__ == "__main__":
    app.run(debug=True)
