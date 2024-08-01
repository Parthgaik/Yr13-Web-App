from flask import Flask, render_template, abort
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



@app.route("/arenas/<int:id>")
def arenas(id):
    maximum_idarenas = connect_database("SELECT MAX(id) FROM Arena")
    if id > maximum_idarenas[0][0]:
        abort(404)
    if id < minimum_idarenas:
        abort(404)
    return render_template("arenas.html", title=card[0][1])


minimum_idarena = 4

@app.route("/arena/<int:id>")
def arena(id):
    maximum_idarena = connect_database("SELECT MAX(id) FROM Arena")
    if id > maximum_idarena[0][0]:
        abort(404)
    if id < minimum_idarena:
        abort(404)
    arena = connect_database("SELECT id, name, Description, Image FROM Arena WHERE id = ?", (id,))
    print(arena)
    return render_template("arena.html", title=arena[0][1], arena=arena[0])


@app.route("/cardtype")
def cardtype():
    return render_template("cardtype.html")


minimum_idcards = 1

@app.route("/allcards/<int:id>")
def allcards(id):
    maximum_idcards = connect_database("SELECT MAX(id) FROM Rarity")
    if id > maximum_idcards[0][0]:
        abort(404)
    if id < minimum_idcards:
        abort(404)
    allcards = connect_database("SELECT id, name, Image FROM Cards WHERE Rarity = ?", (id,))
    rarity= connect_database("SELECT MAX(id) FROM Rarity")
    return render_template("allcards.html", title="All Cards", cards=allcards, id=id, rarity=rarity)


minimum_idcards = 1

@app.route("/card/<int:id>")
def card(id):
    maximum_idcards = connect_database("SELECT MAX(id) FROM Cards")
    if id > maximum_idcards[0][0]:
        abort(404)
    if id < minimum_idcards:
        abort(404)
    card = connect_database("SELECT id, name, Image, description, TypeID FROM Cards WHERE id = ?", (id,))
    counters = connect_database("SELECT Cards.Name, Cards.Image, Counters.CounterID FROM Counters JOIN Cards ON Counters.CounterID = Cards.id WHERE CardID = ?", (id,))
    print(card)
    return render_template("card.html", title=card[0][1], card=card[0], counters=counters, id=id)


@app.errorhandler(404)
def pagenotfound(e):
    return render_template("/404.html", error=e),404
    


if __name__ == "__main__":
    app.run(debug=True)
