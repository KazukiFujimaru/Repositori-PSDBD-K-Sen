import sqlite3

DB_NAME = 'contoh.db'

def buat_tabel():
    query = '''
    CREATE TABLE IF NOT EXISTS tb_kontak (
        id_kontak INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        no_hp TEXT NOT NULL
    )
    '''
    eksekusi_ubah(query)

def eksekusi_ubah(query, parameter=()):
    """Digunakan untuk INSERT, UPDATE, dan DELETE"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, parameter)
    conn.commit()
    jumlah_berubah = cursor.rowcount
    conn.close()
    return jumlah_berubah

def eksekusi_baca(query, parameter=()):
    """Digunakan murni untuk SELECT"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, parameter)
    hasil = cursor.fetchall()
    conn.close()
    return hasil