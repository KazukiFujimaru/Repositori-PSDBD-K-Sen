import sqlite3

# Nama database referensi
DB_NAME = 'contoh.db'

def setup_database():
    """Membuat tabel jika belum ada"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_kontak (
            id_kontak INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            no_hp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def tambah_data():
    nama = input("Masukkan Nama: ")
    no_hp = input("Masukkan No HP: ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Menggunakan (?) untuk mencegah SQL Injection
    cursor.execute("INSERT INTO tb_kontak (nama, no_hp) VALUES (?, ?)", (nama, no_hp))
    conn.commit()
    conn.close()
    print("Berhasil: Kontak baru ditambahkan!")

def tampilkan_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_kontak")
    baris_data = cursor.fetchall()
    conn.close()
    
    print("\n--- DAFTAR KONTAK ---")
    if len(baris_data) == 0:
        print("Data masih kosong.")
    else:
        for baris in baris_data:
            print(f"ID: {baris[0]} | Nama: {baris[1]} | No HP: {baris[2]}")
    print("---------------------")

def edit_data():
    tampilkan_data()
    id_target = input("Masukkan ID kontak yang ingin diedit: ")
    no_hp_baru = input("Masukkan No HP baru: ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tb_kontak SET no_hp = ? WHERE id_kontak = ?", (no_hp_baru, id_target))
    conn.commit()
    
    if cursor.rowcount > 0:
        print("Berhasil: Nomor HP telah diupdate!")
    else:
        print("Gagal: ID tidak ditemukan.")
    conn.close()

def hapus_data():
    tampilkan_data()
    id_target = input("Masukkan ID kontak yang ingin dihapus: ")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_kontak WHERE id_kontak = ?", (id_target,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print("Berhasil: Kontak telah dihapus!")
    else:
        print("Gagal: ID tidak ditemukan.")
    conn.close()

# --- BLOK UTAMA PROGRAM ---
setup_database()
while True:
    print("\n=== MENU BUKU KONTAK ===")
    print("1. Tambah Kontak")
    print("2. Lihat Kontak")
    print("3. Edit No HP")
    print("4. Hapus Kontak")
    print("5. Keluar")
    
    pilihan = input("Pilih menu (1-5): ")
    if pilihan == '1': tambah_data()
    elif pilihan == '2': tampilkan_data()
    elif pilihan == '3': edit_data()
    elif pilihan == '4': hapus_data()
    elif pilihan == '5': break
    else: print("Pilihan salah!")