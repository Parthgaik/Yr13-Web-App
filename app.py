'''Clash Royale Program'''
import sqlite3
from flask import Flask, render_template, abort


app = Flask(__name__)


def connect_database(statement, id=None):
    '''Connection and cursor connect to reduce repeated code'''
    conn = sqlite3.connect("Yr13ClashRoyaleDB.db")
    cursor = conn.cursor()
    #
    if id is not None:
        cursor.execute(statement, id)
    else:
        cursor.execute(statement)
    results = cursor.fetchall()
    conn.close()
    return results


@app.route("/")
def home():
    '''Home page'''
    return render_template("home.html", title="Home")


minimum_idarenas = 4


@app.route("/arenas")
def arenas():
    '''Displaying all arenas page'''
    arenas = connect_database("SELECT id, name, Image FROM Arena")
    return render_template("arenas.html", title="Arenas", arenas=arenas)


minimum_idcardtype = 1


@app.route("/cardtype")
def cardtype():
    '''All cardtypes page'''
    cardtype = connect_database("SELECT id, name, Description, Image FROM Type")
    return render_template("cardtypes.html", title = "Card Types", cardtype=cardtype)


@app.route("/type/<int:id>")
def type(id):
    '''Type of card page'''
    type = connect_database("SELECT * FROM Type WHERE id = ?", (id,))
    return render_template("type.html",title = type[0][1] ,type = type[0])

minimum_idcards = 1


@app.route("/allcards/<int:id>")
def allcards(id):
    '''Displays all cards, error handler applied with the edition of rarity to sort cards by pages so not all the cards are all on one page'''
    maximum_idcards = connect_database("SELECT MAX(id) FROM Rarity")
    if id > maximum_idcards[0][0]:
        abort(404)
    if id < minimum_idcards:
        abort(404)
    allcards = connect_database("SELECT id, name, Image FROM Cards WHERE Rarity = ?", (id,))
    rarity = connect_database("SELECT MAX(id) FROM Rarity")
    return render_template("allcards.html", title="All Cards", cards=allcards, id=id, rarity=rarity)


minimum_idcards = 1

@app.route("/card/<int:id>")
def card(id):
    '''Error handler on single card page, Selecting certain information from card and taking the card counters and joining it into this page'''
    maximum_idcards = connect_database("SELECT MAX(?) FROM Cards", (id,))
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
    '''Error handler'''
    return render_template("/404.html", error=e), 404


if __name__ == "__main__":
    app.run(debug=True)
