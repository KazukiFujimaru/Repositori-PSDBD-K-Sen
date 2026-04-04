import csv

print("=== BACA DATA DARI CSV ===")
try:
    with open('papan_misi.csv', 'r') as file:
        # csv.DictReader otomatis membaca baris pertama sebagai nama kolom (Keys)
        data_misi = csv.DictReader(file) 
        # Untuk cek, silahkan jalankan kode berikut:
        # daftar_misi = list(data_misi)
        # print(daftar_misi)
        
        for misi in data_misi:
            status = "[V]" if misi['status_selesai'] == "true" else "[ ]"
            print(f"{status} | {misi['divisi']} - {misi['nama_misi']}")
except FileNotFoundError:
    print("Error: File papan_misi.csv tidak ditemukan!")