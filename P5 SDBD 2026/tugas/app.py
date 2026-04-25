from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# SEBELUM MEMULAI TUGAS
# Nama tabel dan database bisa diubah
# Nama Database saat ini: playlist_psdbd.db
# Nama Tabel saat ini: tb_playlist

app = Flask(__name__)
DB_NAME = 'playlist_psdbd.db'
# Pastikan playlist_psdbd.db sudah dibuat sebelum melanjutkan.
# Bisa dibuat secara manual atau menggunakan metode yang ada pada sample
# (Cek Web Database [Satu File])

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # TODO 1: Tulis query SELECT untuk mengambil semua data dari tabel tb_playlist
    # songs = conn.execute("...").fetchall()
    
    songs = [] # Hapus atau sesuaikan baris ini setelah TODO 1 dikerjakan
    
    conn.close()
    return render_template('index.html', songs=songs)

@app.route('/add', methods=['POST'])
def add_song():
    judul = request.form['judul']
    penyanyi = request.form['penyanyi']
    genre = request.form['genre']
    pengusul = request.form['pengusul']
    
    conn = get_db_connection()
    # TODO 2: Tulis query INSERT dengan Parameterized Query (?)
    # conn.execute("...", (...))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_song():
    id = request.form['id']
    judul_baru = request.form['judul']
    penyanyi_baru = request.form['penyanyi']
    genre_baru = request.form['genre']
    pengusul_baru = request.form['pengusul']
    
    conn = get_db_connection()
    # TODO 3: Tulis query UPDATE untuk mengubah data berdasarkan ID
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_song(id):
    conn = get_db_connection()
    # TODO 4: Tulis query DELETE berdasarkan ID
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)