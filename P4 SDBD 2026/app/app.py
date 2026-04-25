from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Konfigurasi Database
def get_db(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html')

# FORM 1: No Frontend Warning, No Backend Feedback (Blind Fail)
@app.route('/form1', methods=['GET', 'POST'])
def form1():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        db = get_db('database1.db')
        res = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pw)).fetchone()
        if res:
            return "Login Berhasil (Form 1)"
        # Jika salah, hanya refresh tanpa pesan error (UX Buruk)
        return redirect('/form1') 
    return render_template('form1.html')

# FORM 2: Ada Frontend, Tapi Backend Rentan SQL Injection (Vulnerable)
@app.route('/form2', methods=['GET', 'POST'])
def form2():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        db = get_db('database1.db')
        # KERENTANAN: Menggunakan f-string (SQL Injection target)
        query = f"SELECT * FROM users WHERE username = '{user}' AND password = '{pw}'"
        res = db.execute(query).fetchone()
        if res:
            return f"Login Berhasil! Query yang dijalankan: {query}"
        return "Login Gagal"
    return render_template('form2.html')

# FORM 3: Ada Backend Check, Tapi Error DB ditampilkan Raw (Info Disclosure)
@app.route('/form3', methods=['GET', 'POST'])
def form3():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        try:
            db = get_db('database2.db')
            # Simulasi error constraint (misal: input kosong atau melanggar CHECK)
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pw))
            db.commit()
            return "Data Berhasil Masuk ke DB2"
        except Exception as e:
            # BAHAYA: Menampilkan pesan error asli dari SQLite ke User
            error = str(e) 
    return render_template('form3.html', error=error)

# FORM 4: Ideal (Frontend + Backend + Custom Error)
@app.route('/form4', methods=['GET', 'POST'])
def form4():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        
        # Backend Validation
        if not user or not pw:
            error = "Mohon isi semua kolom dengan benar."
        else:
            db = get_db('database2.db')
            res = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, pw)).fetchone()
            if res:
                return "Login Berhasil (Safe & Clean)"
            else:
                error = "Kredensial salah atau akun tidak ditemukan."
                
    return render_template('form4.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)