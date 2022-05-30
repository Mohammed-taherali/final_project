from flask import render_template, request, Flask
import sqlite3

conn = sqlite3.connect(":memory:")

cr = conn.c

app = Flask(__name__)

@app.route("/")
def index():
    print("first branch")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
# hello world