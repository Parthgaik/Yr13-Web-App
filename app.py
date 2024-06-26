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
    return render_template("allcards.html", title="All Cards", cards=allcards)


@app.route("/card/<int:id>")
def card(id):
    if id > 
    card = connect_database("SELECT id, name, Image, description FROM Cards WHERE id = ?", (id,))
    counters = connect_database("SELECT Cards.Name, Cards.Image FROM Counters JOIN Cards ON Counters.CounterID = Cards.id WHERE CardID = ?", (id,))
    print(card)
    return render_template("card.html", title=card[0][1], card=card[0], counters=counters)


@app.route("/arenas")
def arenas():
    return render_template("arenas.html")


@app.route("/cardtype")
def cardtype():
    return render_template("cardtype.html")


@app.errorhandler(404)
def pagenotfound(e):
    return render_template("/404.html", error=e),404
    


if __name__ == "__main__":
    app.run(debug=True)
