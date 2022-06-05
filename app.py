from flask import flash, render_template, request, Flask, redirect, get_flashed_messages, session
from flask_session import Session
import sqlite3
import logging
from datetime import date
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology
# logging.basicConfig(filename='logging.log',level=logging.CRITICAL,
#                     format= "[%(levelname)s] %(asctime)s - %(message)s")

app = Flask(__name__)

current_dist = {}

username = "taherali"
password = generate_password_hash("jhalrapatan420")

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# db = SQL("sqlite:///shop.db")
def get_db_connection():
    conn = sqlite3.connect("shop.db")
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect("/login")
    else:
        # db.execute("""CREATE TABLE IF NOT EXISTS bills (
        #     invoice_no INTEGER NOT NULL,
        #     dist_name TEXT NOT NULL,
        #     date TEXT,
        #     no_of_items INTEGER
        #     )""")

        # db.execute("""CREATE TABLE IF NOT EXISTS distributor_info (
        #     dist_id TEXT primary key,
        #     dist_name TEXT NOT NULL,
        #     contact_no TEXT NOT NULL
        #     )""")

        conn = get_db_connection()
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS bills (
                        invoice_no INTEGER NOT NULL,
                        dist_name TEXT NOT NULL,
                        date TEXT,
                        no_of_items INTEGER
                        )""")

            c.execute("""CREATE TABLE IF NOT EXISTS distributor_info (
                        dist_id TEXT primary key,
                        dist_name TEXT NOT NULL,
                        contact_no TEXT NOT NULL
                        )""")

        return render_template("index.html", level="primary")
        #this is the latest and working version

@app.route("/addBill", methods=["GET", "POST"])
def addBill():
    if request.method == "GET":
        return render_template("addbill.html", current_date = date.today().strftime("%d/%m/%Y"), level="primary")
    else:
        if request.form.get("distName") and request.form.get("date") and request.form.get("items"):
            current_dist["distName"] = request.form.get("distName")
            current_dist["date"] = request.form.get("date")
            try:
                current_dist["no_of_items"] = int(request.form.get("items"))
            except ValueError:
                flash("Please enter an integer number!")
                return render_template("addbill.html", level="warning")

        else:
            flash("Please fill in all the fields!")
            return render_template("addbill.html", level="warning")

        # if not db.execute("SELECT * FROM distributor_info WHERE dist_name = ?", current_dist['distName']):
        conn = get_db_connection()
        c = conn.cursor()
        if not c.execute("SELECT * FROM distributor_info WHERE dist_name = ?", (current_dist['distName'],)):
            flash("This distributor is not added to your list of distributors! Please add them and try again!")
            return render_template("addbill.html", level="warning")
        return redirect("/additems")


@app.route("/additems", methods=["GET", "POST"])
def additems():
    """
    This function adds the items entered to the respective bill
    """

    if request.method == "POST":
        bill_items = []
        for bill in range(current_dist["no_of_items"]):
            bills = {}
            bills["medName"] = request.form.get(f"medName{bill}")
            bills["quantity"] = int(request.form.get(f"quantity{bill}"))
            bills["expiry"] = request.form.get(f"expiry{bill}")
            bills["rate"] = float(request.form.get(f"rate{bill}"))
            bills["mrp"] = float(request.form.get(f"mrp{bill}"))
            bill_items.append(bills)
        print(bill_items)
        return redirect("/")
    elif request.method == "GET":
        current_date = date.today().strftime("%d/%m/%Y")
        return render_template("addbill.html", current_date=current_date, no_of_items=current_dist["no_of_items"], level="primary", current_dist=current_dist)

@app.route("/addDist", methods=["GET", "POST"])
def addDist():
    # If user has reached through get request (button click or changing the url)
    if request.method == "GET":
        # conn = get_db_connection()
        # c = conn.cursor()
        # with conn:
        #     distributors = c.execute("SELECT * from distributor_info")
        return render_template("addDist.html", level="primary")

    # else user has reached here by submitting the form
    else:

        # Get the user inputs and validate them
        conn = get_db_connection()
        c = conn.cursor()

        distName = request.form.get("distName").strip().upper()
        distId = request.form.get("distId").strip().upper()
        distContact = request.form.get("distContact").strip().upper()

        distributors = c.execute("SELECT * from distributor_info")

        if not distName or not distId or not distContact:
            flash("Please fill in all the details!")
            return render_template("addDist.html", level="warning", distributors=distributors)

        if c.execute("SELECT dist_name FROM distributor_info WHERE dist_name = ?", (distName,)).fetchone():
            flash("Distributor with this name exists!")
            return render_template("addDist.html", level="warning")

        if c.execute("SELECT * FROM distributor_info WHERE dist_id = ?", (distId,)).fetchone():
            flash("Please add a unique distributor Id!")
            return render_template("addDist.html", level="warning")

        # Check if distributor with the same name exists or not.
        # else insert value into distributor_info table.
        # existing_dist = c.execute("SELECT dist_name FROM distributor_info WHERE dist_name = ?", (distName,)).fetchone()
        # print(existing_dist )
        # print("above is exit dist")

        # if existing_dist:
        #     print("not inserting!")
        #     flash("Distributor with this name exists!")
        #     return render_template("addDist.html", level="warning")
            #this is good part
            # print("inserting latest row")
            # with conn:
            #     c.execute("INSERT INTO distributor_info(dist_id, dist_name, contact_no) values(?, ?, ?)", (distId.strip().upper(), distName.strip().upper(), distContact))

        print("inserting latest row")
        with conn:
            c.execute("INSERT INTO distributor_info(dist_id, dist_name, contact_no) values(?, ?, ?)", (distId.strip().upper(), distName.strip().upper(), distContact))
            # print("not inserting!")
            # flash("Distributor with this name exists!")
            # return render_template("addDist.html", level="warning")

        # distributors = c.execute("SELECT * FROM distributor_info")

        flash("Distributor added successfully!")
        return redirect("/distInfo")


@app.route("/distInfo", methods=["GET"])
def distInfo():
    conn = get_db_connection()
    c = conn.cursor()
    distributors = c.execute("SELECT * FROM distributor_info").fetchall()
    print(distributors)
    return render_template("distInfo.html", level="primary", distributors=distributors)

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Please enter username and/or password!")

        if request.form.get("username") != username or not check_password_hash(password, request.form.get("password")):
            return apology("Incorrect Id and/or password!")

        else:
            session["username"] = username
            session["password"] = request.form.get("password")

            flash("Succesfully logged In!")
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