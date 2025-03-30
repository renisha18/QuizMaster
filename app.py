from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# Connect to the database
db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    return f"Connected successfully! Tables: {tables}"

if __name__ == "__main__":
    app.run(debug=True)