'''Clash Royale Program'''
import sqlite3
from flask import Flask, render_template, abort


app = Flask(__name__)


def connect_database(statement, id=None, fetch_all=True):
    '''Connection and cursor connect to reduce repeated code'''
    conn = sqlite3.connect("Yr13ClashRoyaleDB.db")
    cursor = conn.cursor()
    # When an id is given to the function, the results are fetched through either a fetchall or fetchone
    # Making an if fetch_all loop in case both fetchall or fetchone are required
    if id is not None:
        cursor.execute(statement, id)
    else:
        cursor.execute(statement)
    if fetch_all:
        results = cursor.fetchall()
    else:
        results = cursor.fetchone()
    conn.close()
    return results


def get_max_id(table_name):
    '''Finding the maximum id of a query'''
    # Using the result of the function, turing it into a string using the f string and running it through the query
    # Making sure there is actually a result from the if result[0] loop
    query = f"SELECT MAX(id) FROM {table_name}"
    result = connect_database(query, fetch_all=False)
    if result[0] is not None:
        return result[0]
    else:
        return 0


@app.route("/")
def home():
    '''Home page'''
    return render_template("home.html", title="Home")


minimum_idarenas = 4


@app.route("/arenas")
def arenas():
    '''Displaying all arenas page'''
    # Selecting all items from the id, name, image columns from the arena table into the query and displaying it onto the website
    arenas = connect_database("SELECT id, name, Image FROM Arena")
    return render_template("arenas.html", title="Arenas", arenas=arenas)


minimum_idcardtype = 1


@app.route("/cardtype")
def cardtype():
    '''All cardtypes page'''
    # Selecting all items from the id, name, image, description columns from the type 
    # table into the query and displaying it onto the website
    cardtype = connect_database("SELECT id, name, Description, Image FROM Type")
    return render_template("cardtypes.html", title = "Card Types", cardtype=cardtype)


@app.route("/type/<int:id>")
def type(id):
    '''Type of card page'''
    # Error prevention in function
    # Using the get_max_id function for type, seeing if the value of it is larger than the id retrieved from the user, if so, abort the 404 page
    # otherwise return the items within the range onto the webpage
    # 'If not type' is for if id retireved is within the range of maximum id but does not exist in database
    max_id = get_max_id("Type")
    if id > max_id:
        abort(404)
    type = connect_database("SELECT * FROM Type WHERE id = ?", (id,))
    if not type:
        abort(404)
    return render_template("type.html",title = type[0][1] ,type = type[0])

minimum_idcards = 1


@app.route("/allcards/<int:id>")
def allcards(id):
    '''Displays all cards, error handler applied with the edition of rarity to sort cards by pages so not all the cards are all on one page'''
    # Error prevention in function
    # The query with the rarity is for the sorting of my items on the webpage, decided to sort the items by rarity
    # Using the get_max_id function for rarity, seeing if the value of it is larger than the id retrieved from the user, if so, abort the 404 page
    # otherwise return the items within the range onto the webpage
    # 'If not type' is for if id retireved is within the range of maximum id but does not exist in database
    maximum_idcards = connect_database("SELECT MAX(id) FROM Rarity")
    if id > maximum_idcards[0][0]:
        abort(404)
    if id < minimum_idcards:
        abort(404)
    allcards = connect_database("SELECT id, name, Image FROM Cards WHERE Rarity = ?", (id,))
    rarity = connect_database("SELECT MAX(id) FROM Rarity")
    return render_template("allcards.html", title="All Cards", cards=allcards, id=id, rarity=rarity)


@app.route("/card/<int:id>")
def card(id):
    '''Error handler on single card page, Selecting certain information from card and taking the card counters and joining it into this page'''
    # Error prevention in function
    # Using the get_max_id function for Cards, seeing if the value of it is larger than the id retrieved from the user, if so, abort the 404 page
    # otherwise return the items within the range onto the webpage
    # counters variable is for displaying all the counters for a certain card, joining other parts of tables onto the query
    max_id = get_max_id("Cards")
    if id > max_id:
        abort(404)
    card = connect_database("SELECT id, name, Image, description, TypeID FROM Cards WHERE id = ?", (id,))
    if not card:
        abort(404)
    counters = connect_database("SELECT Cards.Name, Cards.Image, Counters.CounterID FROM Counters JOIN Cards ON Counters.CounterID = Cards.id WHERE CardID = ?", (id,))
    return render_template("card.html", title=card[0][1], card=card[0], counters=counters, id=id)


@app.errorhandler(404)
def pagenotfound(e):
    '''Error handler'''
    # Handles errors
    return render_template("/404.html", error=e), 404

# :)
if __name__ == "__main__":
    app.run(debug=True)
