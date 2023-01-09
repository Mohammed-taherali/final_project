THIS IS MY CS50's FINAL PROJECT!

STORE MANAGER

This application uses python as the backend language along with sqlite 3 database to store data.
The frontend includes HTML, CSS and JavaScript.

The purpose of this application is to manage all the products of your store.
It is primarily suited for medical shops/Pharmacies.

The main database of the program is called 'shop.db'.
Its Schema is as follows:
CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT 
                        user_name TEXT NOT NULL 
                        hash TEXT NOT NULL
                        );
CREATE TABLE sqlite_sequence(name seq);
CREATE TABLE distributor_info (
                        id INTEGER NOT NULL 
                        dist_id TEXT primary key 
                        dist_name TEXT UNIQUE NOT NULL 
                        contact_no TEXT NOT NULL 
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        );
CREATE TABLE bills (
                        id INTEGER 
                        invoice_no TEXT PRIMARY KEY 
                        dist_name TEXT NOT NULL 
                        date TEXT NOT NULL 
                        no_of_items INTEGER NOT NULL 
                        FOREIGN KEY(dist_name) REFERENCES distributor_info(dist_name) 
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        );
CREATE TABLE med_details(
                        id INTEGER 
                        med_no INTEGER PRIMARY KEY AUTOINCREMENT 
                        med_name TEXT NOT NULL 
                        rate REAL 
                        mrp REAL NOT NULL 
                        expiry TEXT NOT NULL 
                        quantity INTEGER NOT NULL 
                        total REAL NOT NULL 
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        );
CREATE TABLE bill_info (
                        id INTEGER NOT NULL 
                        invoice_no TEXT 
                        med_name TEXT 
                        quantity INTEGER NOT NULL 
                        FOREIGN KEY(id) REFERENCES users(user_id) 
                        FOREIGN KEY(invoice_no) REFERENCES bills(invoice_no) 
                        FOREIGN KEY(med_name) REFERENCES med_details(med_name)
                        );
CREATE TABLE cart (
                        id INTEGER NOT NULL 
                        med_name TEXT NOT NULL 
                        quantity INTEGER NOT NULL 
                        total REAL NOT NULL 
                        dist_name TEXT 
                        FOREIGN KEY(id) REFERENCES users(user_id)
                        );
CREATE INDEX med_info ON med_details(med_name  rate  mrp  expiry  quantity);
CREATE INDEX bill_details ON bill_info(id  invoice_no  med_name);
CREATE INDEX bill_no ON bills(id  invoice_no  dist_name  date  no_of_items);


The main 'app.py' file has 13 routes.

1] '/' route (homepage/ index page)

    This page contains all the products contained in the shop. It lists the products (by default) according to the ascending order of the product name. However the 2 more options are available 
    i) Order by Expiry date (ascending)
    ii) Order by Expiry date (descending)

    The user can also add a particular medicine which is available at the store to the cart to buy it from the distributor.


2] '/addBill' route

    This page adds the bill of purchase from the distributor.

    The bill details include Invoice number, Distributor name, Date of purchase, Number of items in the bill.
    After filling this information, the user can add the details of individual product.


3] '/showBills' route

    It shows all the purchases of the user with details of all bills.


4] '/additems' route 

    This route is called internally by the '/addBill' route to add the details of every product in that respective bill.
    
    Details of products include Product name, Quantity, Rate, MRP, Expiry.


5] '/addToCart' route

    This route adds the items already available with the user to the cart to purchase it from the distributor.


6] '/cart' route

    This route displays all the items present in the cart.
    It also shows the total estimated bill amount.


7] '/addMed' route

    This method is called when a medicine is added from homepage.
    It modifies the med_details table of the shop.db database.

8] '/addDist' route

    It adds new distributor for the current user.

9] '/distInfo' route

    It displays the distributors for the current user.


10] '/removeDist' route

    Called on clicking the 'remove dist' button on the distInfo page.
    It deletes the respective distributor from the list of distributors for the user.

11] '/login' route

    Logs a valid user in.
    It uses check_password_hash and generate_password_hash functions from the werkzeug.security library.


12] '/logout' route

    Logs a user out by deleting the session details and redirects the user to login page


13] '/register' route

    Registers a new valid user.


My name is Mohammed Taherali and this was CS50!
