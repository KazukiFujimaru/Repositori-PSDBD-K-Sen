from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'contoh.db'

# Fungsi inisialisasi database (Dijalankan saat file di-run)
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tb_kontak (
                        id_kontak INTEGER PRIMARY KEY AUTOINCREMENT,
                        nama TEXT NOT NULL,
                        no_hp TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # READ: Menampilkan data
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_kontak")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data_kontak=data)

@app.route('/tambah', methods=['POST'])
def tambah():
    # CREATE: Menangkap form dan insert ke database
    nama = request.form['input_nama']
    nohp = request.form['input_nohp']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tb_kontak (nama, no_hp) VALUES (?, ?)", (nama, nohp))
    conn.commit()
    conn.close()
    return redirect('/') # Kembali ke halaman utama

@app.route('/edit/<id_target>')
def edit_tampilan(id_target):
    # READ 1 DATA: Mengambil data lama untuk ditampilkan di form HTML
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_kontak WHERE id_kontak = ?", (id_target,))
    data = cursor.fetchone()
    conn.close()
    return render_template('edit.html', data_lama=data)

@app.route('/edit_proses', methods=['POST'])
def edit_proses():
    # UPDATE: Menyimpan data baru
    id_target = request.form['input_id']
    nama_baru = request.form['input_nama']
    nohp_baru = request.form['input_nohp']
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_kontak SET nama = ?, no_hp = ? WHERE id_kontak = ?", (nama_baru, nohp_baru, id_target))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/hapus/<id_target>')
def hapus(id_target):
    # DELETE: Menghapus data
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_kontak WHERE id_kontak = ?", (id_target,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)