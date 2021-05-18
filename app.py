from flask import Flask, render_template
import requests
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    con = sqlite3.connect('vantest.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM vans ORDER BY price")

    rows = cur.fetchall()
    return render_template('index.html', rows = rows)

if __name__ == '__main__':
    app.run(debug=True)