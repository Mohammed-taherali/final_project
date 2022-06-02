from flask import flash, render_template, request, Flask, redirect, get_flashed_messages, session
from flask_session import Session
import sqlite3
import logging
from datetime import date

from importlib_metadata import method_cache

from helpers import apology
# logging.basicConfig(filename='logging.log',level=logging.CRITICAL,
#                     format= "[%(levelname)s] %(asctime)s - %(message)s")
conn = sqlite3.connect(":memory:")

c = conn.cursor()

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

c.execute("""CREATE TABLE bills (
            invoice_no INTEGER NOT NULL,
            dist_name TEXT NOT NULL,
            date TEXT,
            no_of_items INTEGER
            )""")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect("/login")
    else:
        flash("Succesfully logged In!")
        return render_template("index.html")

@app.route("/addBill")
def addBill():
    if request.method == "GET":
        return render_template("addbill.html", current_date = date.today().strftime("%d/%m/%Y"))

@app.route("/additems", methods=["GET", "POST"])
def additems():
    """
    This function adds the items entered to the respective bill
    """

    if request.method == "POST":
        dist_name = request.form.get("distName")
        currrent_date = request.form.get("date")
        no_of_items = int(request.form.get("items"))
        return render_template("addbill.html", no_of_items=no_of_items )

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        session["username"] = "taherali"
        session["password"] = "jhalrapatan420"
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Please enter username and/or password!")
        
        if request.form.get("username") != "taherali" or request.form.get("password") != "jhalrapatan420":
            return apology("Incorrect Id and/or password!")

        else:
            return redirect("/")
    elif request.method == "GET":
        return render_template("login.html")

@app.route("/logout")
def logout():
    session["username"] = None
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
