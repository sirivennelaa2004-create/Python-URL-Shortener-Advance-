from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

create_table()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_code = generate_short_code()

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
            (original_url, short_code)
        )
        conn.commit()
        conn.close()

        short_url = request.host_url + short_code
        return render_template('result.html', short_url=short_url)

    return render_template('index.html')


@app.route('/<short_code>')
def redirect_url(short_code):
    conn = get_db_connection()
    url_data = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()
    conn.close()

    if url_data:
        return redirect(url_data['original_url'])
    else:
        return "URL not found", 404


if __name__ == '__main__':
    app.run(debug=True)