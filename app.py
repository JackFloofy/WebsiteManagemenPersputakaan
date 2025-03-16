from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = sqlite3.connect('bookings.db')
    conn.row_factory = sqlite3.Row  
    return conn

# Inisialisasi database
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL
        )
    ''')

    conn.close()

# Route halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('index.html', bookings=bookings)

# Route untuk menambah data
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    book_id = request.form['book_id']
    email = request.form['email']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if name and book_id and email and start_date and end_date:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (name, book_id, email, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                     (name, book_id, email, start_date, end_date))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

# Route untuk menghapus data
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM bookings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
