from flask import flash, render_template, request, Flask, redirect, get_flashed_messages, session
from flask_session import Session
import sqlite3
import logging
from datetime import date
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

logging.basicConfig(filename='logging.log',level=logging.CRITICAL,
                    format= "[%(levelname)s] %(asctime)s - %(message)s")

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

current_dist = {}


# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# db = SQL("sqlite:///shop.db")
def get_db_connection():
    conn = sqlite3.connect("shop.db")
    return conn


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if not session.get("user_id"):
        return redirect("/login")
    
    else:

        conn = get_db_connection()
        c = conn.cursor()
        with conn:
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT UNIQUE NOT NULL,
                        hash TEXT NOT NULL
                        )""")

            c.execute("""CREATE TABLE IF NOT EXISTS distributor_info (
                        id INTEGER NOT NULL,
                        dist_id TEXT primary key,
                        dist_name TEXT UNIQUE NOT NULL,
                        contact_no TEXT NOT NULL,
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        )""")

            c.execute("""CREATE TABLE IF NOT EXISTS bills (
                        id INTEGER,
                        invoice_no TEXT PRIMARY KEY,
                        dist_name TEXT NOT NULL,
                        date TEXT NOT NULL,
                        no_of_items INTEGER NOT NULL,
                        FOREIGN KEY(dist_name) REFERENCES distributor_info(dist_name),
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        )""")

            c.execute("""CREATE TABLE IF NOT EXISTS med_details(
                        id INTEGER,
                        med_no INTEGER PRIMARY KEY AUTOINCREMENT,
                        med_name TEXT NOT NULL,
                        rate REAL,
                        mrp REAL NOT NULL,
                        expiry TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        )""")

            """CREATE TABLE IF NOT EXISTS med_details(
                id INTEGER,
                med_no INTEGER PRIMARY KEY AUTOINCREMENT,
                med_name TEXT NOT NULL,
                rate REAL,
                mrp REAL NOT NULL,
                expiry TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                # New part
                total REAL NOT NULL,
                FOREIGN KEY(id) REFERENCES users(user_id)
                )"""

            c.execute("""CREATE TABLE IF NOT EXISTS bill_info (
                        id INTEGER NOT NULL,
                        invoice_no TEXT,
                        med_name TEXT,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY(id) REFERENCES users(user_id),
                        FOREIGN KEY(invoice_no) REFERENCES bills(invoice_no),
                        FOREIGN KEY(med_name) REFERENCES med_details(med_name)
                        )""")
                    
            c.execute("""CREATE TABLE IF NOT EXISTS cart (
                        id INTEGER NOT NULL,
                        med_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        total REAL NOT NULL,
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        )""")

        medicines = c.execute("SELECT med_name, expiry, rate, mrp, quantity, med_no FROM med_details WHERE id = ?", (session["user_id"],)).fetchall()
        

        return render_template("index.html", level="primary", medicines=medicines)
        #this is the latest and working version


@app.route("/addBill", methods=["GET", "POST"])
@login_required
def addBill():
    """
    This function adds new bills to the database.
    """

    current_date = date.today().strftime("%Y-%m-%d")

    # Render template to enter the bill details
    if request.method == "GET":
        return render_template("addbill.html", current_date = current_date)
    
    # Else user has entered the bill details
    else:

        # Connect to the database.
        conn = get_db_connection()
        c = conn.cursor()

        # Validate the details and update the database
        current_dist["invoiceNo"] = request.form.get("invoiceNo").strip().upper()
        current_dist["distName"] = request.form.get("distName").strip().upper()
        current_dist["date"] = request.form.get("date").strip()
        try:
            current_dist["no_of_items"] = int(request.form.get("items").strip())
        except ValueError:
            flash("Please enter an integer number!")
            return render_template("addbill.html", level="warning")

        if current_dist["distName"] and current_dist["date"] and current_dist["no_of_items"] and current_dist["invoiceNo"]:

            if not c.execute("SELECT * FROM distributor_info WHERE dist_name = ? and id = ?", (current_dist["distName"], session["user_id"])).fetchone():

                flash("This distributor is not added to your list of distributors! Please add them and try again!")
                return render_template("addbill.html", level="warning")

            if c.execute("SELECT * FROM bills where invoice_no = ? and id = ?", (current_dist["invoiceNo"], session["user_id"])).fetchone():
                flash("Bill with this Invoice number exists!")
                return render_template("addbill.html", level="warning", current_date=current_date)

        else:
            flash("Please fill in all the fields!")
            return render_template("addbill.html", level="warning", current_date=current_date)

        return redirect("/additems")


@app.route("/showBills", methods=["GET"])
@login_required
def showBills():

    # Connect to database.
    conn = get_db_connection()
    c = conn.cursor()

    bills = c.execute("SELECT invoice_no, dist_name, date, no_of_items FROM bills WHERE id = ?", (session["user_id"],)).fetchall()

    return render_template("billInfo.html", bills=bills)


@app.route("/additems", methods=["GET", "POST"])
@login_required
def additems():
    """
    This function adds the items entered to the respective bill
    """
    if request.method == "POST":

        conn = get_db_connection()
        c = conn.cursor()

        tax = 0.12
        bill_items = []
        for bill in range(current_dist["no_of_items"]):
    
            if not request.form.get(f"medName{bill}") or not \
            request.form.get(f"quantity{bill}") or not \
            request.form.get(f"expiry{bill}") or not \
            request.form.get(f"rate{bill}") or not \
            request.form.get(f"mrp{bill}"):

                flash("Please enter all the details!")
                return render_template("addbill.html", level="warning", \
                current_date=current_dist["date"], current_dist=current_dist,\
                no_of_items=current_dist["no_of_items"])

            bills = {}
            bills["medName"] = request.form.get(f"medName{bill}").strip().upper()
            bills["expiry"] = request.form.get(f"expiry{bill}")
            try:
                bills["quantity"] = int(request.form.get(f"quantity{bill}"))
                bills["rate"] = float(request.form.get(f"rate{bill}"))
                bills["mrp"] = float(request.form.get(f"mrp{bill}"))
            except ValueError:
                flash("Please enter an integer or decimal number!")
                return render_template("addbill.html", level="warning", \
                current_dist=current_dist)

            bill_items.append(bills)

        with conn:
            c.execute("INSERT INTO bills(id, invoice_no, dist_name, date, no_of_items) VALUES(?,?,?,?,?)", 
            (session["user_id"], current_dist["invoiceNo"], current_dist["distName"], current_dist["date"], current_dist["no_of_items"]))

            for item in bill_items:

                if c.execute("SELECT * FROM med_details WHERE med_name = ? and id = ?", (item["medName"], session["user_id"])).fetchone():
                    price = c.execute("SELECT mrp FROM med_details WHERE med_name = ? and id = ?", (item["medName"], session["user_id"])).fetchone()[0] 
                    expiry = c.execute("SELECT expiry FROM med_details WHERE med_name = ? and id = ?", (item["medName"], session["user_id"])).fetchone()[0]

                    if price == item["mrp"] and expiry == item["expiry"]:
                        existing_quantity = int(c.execute("SELECT quantity FROM med_details WHERE med_name = ? and id = ?", (item["medName"], session["user_id"])).fetchone()[0])
                        c.execute("UPDATE med_details SET quantity = ? WHERE med_name = ? and id = ?", (existing_quantity + item["quantity"], item["medName"], session["user_id"]))

                    else:
                        c.execute("INSERT INTO med_details(id, med_name, rate, mrp, expiry, quantity) VALUES(?,?,?,?,?,?)", 
                        (session["user_id"], item["medName"], item["rate"] + tax * item["rate"], item["mrp"], item["expiry"], item["quantity"]))

                else:
                    c.execute("INSERT INTO med_details(id, med_name, rate, mrp, expiry, quantity) VALUES(?,?,?,?,?,?)", 
                    (session["user_id"], item["medName"], item["rate"] + tax * item["rate"], item["mrp"], item["expiry"], item["quantity"]))

                c.execute("INSERT INTO bill_info(id, invoice_no, med_name, quantity) VALUES(?,?,?,?)", 
                (session["user_id"], current_dist["invoiceNo"], item["medName"], item["quantity"]))

        return redirect("/")
        
    elif request.method == "GET":
        try:
            return render_template("addbill.html", level="primary", \
            current_dist=current_dist)
        except KeyError:
            return redirect("/addBill")


@app.route("/addToCart", methods=["GET"])
@login_required
def addToCart():
    if request.method == "GET":
        quantity = request.args.get("quantity")
        med_no = request.args.get("current_row_index")

        conn = get_db_connection()
        c = conn.cursor()

        med_name = c.execute("SELECT med_name FROM med_details WHERE id = ? and med_no = ?", (session["user_id"], med_no)).fetchone()[0]
        print(med_name)
        # distributor_name = c.execute("SELECT")

        """CREATE TABLE IF NOT EXISTS cart (
            id INTEGER NOT NULL,
            med_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY(id) REFERENCES users(user_id)
            )"""
        
        flash("Item successfully added to cart!")
        return redirect("/")


@app.route("/addDist", methods=["GET", "POST"])
@login_required
def addDist():

    # If user has reached through get request (button click or changing the url)
    if request.method == "GET":
    
        return render_template("addDist.html", level="primary")

    # else user has reached here by submitting the form
    else:

        # Get the user inputs and validate them
        conn = get_db_connection()
        c = conn.cursor()

        distName = request.form.get("distName").strip().upper()
        distId = request.form.get("distId").strip().upper()
        distContact = request.form.get("distContact").strip().upper()

        distributors = c.execute("SELECT * FROM distributor_info WHERE id = ?", (session["user_id"], )).fetchall()

        if not distName or not distId or not distContact:
            flash("Please fill in all the details!")
            return render_template("addDist.html", level="warning")

        if c.execute("SELECT dist_name FROM distributor_info WHERE dist_name = ? and id = ?", (distName, session["user_id"])).fetchone():
            flash("Distributor with this name exists!")
            return render_template("addDist.html", level="warning")

        if c.execute("SELECT * FROM distributor_info WHERE dist_id = ? and id + ?", (distId, session["user_id"])).fetchone():
            flash("Please add a unique distributor Id!")
            return render_template("addDist.html", level="warning")

        with conn:
            c.execute("INSERT INTO distributor_info(id, dist_id, dist_name, contact_no) values(?, ?, ?, ?)", (session["user_id"], distId.strip().upper(), distName.strip().upper(), distContact))

        flash("Distributor added successfully!")
        return redirect("/distInfo")


@app.route("/distInfo", methods=["GET"])
@login_required
def distInfo():
    conn = get_db_connection()
    c = conn.cursor()
    distributors = c.execute("SELECT dist_id, dist_name, contact_no FROM distributor_info where id = ?", (session["user_id"],)).fetchall()
    return render_template("distInfo.html", level="primary", distributors=distributors)


@app.route("/removeDist", methods=["GET", "POST"])
@login_required
def removeDist():
    distributor_id = list(request.form)[0]
    
    conn = get_db_connection()
    c = conn.cursor()

    with conn:
        c.execute("DELETE FROM distributor_info WHERE dist_id = ?", (distributor_id,))

    flash("Distributor removed succesfully!")
    return redirect("/distInfo")


@app.route("/test")
@login_required
def test():

    conn = get_db_connection()
    c = conn.cursor()
    test = c.execute("SELECT * FROM distributor_info ORDER BY contact_no").fetchall()
    print(test)
    return render_template("test.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in""" 

    # Forget any user
    session.clear()

    # User reached route via POST (as by submitting a form)
    if request.method == "POST":

        # Get connection to database
        conn = get_db_connection()
        c = conn.cursor()

        # Ensure all fields exist
        if not request.form.get("username") or not request.form.get("password"):
            return apology("Please enter username and/or password!")

        # Check password
        try:
            hash_password = c.execute("SELECT hash FROM users WHERE user_name = ?", (request.form.get("username").strip(),)).fetchone()[0]
        except TypeError:
            flash("Invalid username and/or password!")
            return render_template("login.html", level="primary")

        if not check_password_hash(hash_password, request.form.get("password")):
            # print(hash_password, request.form.get("password"))
            flash("Invalid username and/or password!")
            return render_template("login.html", level="primary")

        # Remember which user has logged in
        session["user_id"] = int(c.execute("SELECT user_id FROM users WHERE user_name = ?", (request.form.get("username"),)).fetchone()[0])
        session["username"] = request.form.get("username").strip()

        flash("Successfully logged In!")
        return redirect("/")

    elif request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    # session["username"] = None
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":

        conn = get_db_connection()
        c = conn.cursor()

        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            flash("PLEASE FILL IN ALL THE FIELDS!")
            return render_template("register.html", level="danger")

        if c.execute("SELECT * FROM users WHERE user_name = ?", (request.form.get("username").strip(), )).fetchone():
            flash("This username is not available please try some other username!")
            return render_template("register.html", level="danger")

        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password and confirm password fields are not same!")
            return render_template("register.html", level="danger")

        user_name = request.form.get("username").strip()
        user_password = generate_password_hash(request.form.get("password"))

        # If all details are valid then register the user
        with conn:
            c.execute("INSERT INTO users(user_name, hash) values(?, ?)", (user_name, user_password))
        
        flash("Successfully Registered!")
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
