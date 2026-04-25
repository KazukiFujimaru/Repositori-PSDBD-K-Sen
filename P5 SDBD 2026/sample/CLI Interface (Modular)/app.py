# Import script python 'database' agar kita bisa mengakses fungsi yang ada di database.py
import database 

def tambah_data():
    nama = input("Masukkan Nama: ")
    no_hp = input("Masukkan No HP: ")
    query = "INSERT INTO tb_kontak (nama, no_hp) VALUES (?, ?)"
    database.eksekusi_ubah(query, (nama, no_hp))
    print("Berhasil ditambahkan!")

def tampilkan_data():
    query = "SELECT * FROM tb_kontak"
    data = database.eksekusi_baca(query)
    print("\n--- DAFTAR KONTAK ---")
    for baris in data:
        print(f"[{baris[0]}] {baris[1]} - {baris[2]}")

def edit_data():
    tampilkan_data()
    id_target = input("ID kontak yang diedit: ")
    hp_baru = input("No HP baru: ")
    query = "UPDATE tb_kontak SET no_hp = ? WHERE id_kontak = ?"
    hasil = database.eksekusi_ubah(query, (hp_baru, id_target))
    if hasil > 0: print("Berhasil diedit!")
    else: print("ID tidak ditemukan.")

def hapus_data():
    tampilkan_data()
    id_target = input("ID kontak yang dihapus: ")
    query = "DELETE FROM tb_kontak WHERE id_kontak = ?"
    hasil = database.eksekusi_ubah(query, (id_target,))
    if hasil > 0: print("Berhasil dihapus!")
    else: print("ID tidak ditemukan.")

# --- BLOK UTAMA PROGRAM ---
database.buat_tabel()
while True:
    print("\n1. Tambah | 2. Lihat | 3. Edit | 4. Hapus | 5. Keluar")
    pilihan = input("Pilih menu: ")
    if pilihan == '1': tambah_data()
    elif pilihan == '2': tampilkan_data()
    elif pilihan == '3': edit_data()
    elif pilihan == '4': hapus_data()
    elif pilihan == '5': break