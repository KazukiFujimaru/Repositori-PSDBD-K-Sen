import json

print("=== BACA DATA DARI JSON ===")
try:
    with open('papan_misi.json', 'r') as file:
        # Membaca seluruh file menjadi List of Dictionary (stuktur data)
        data_misi = json.load(file) 
        # Untuk cek, silahkan jalankan kode berikut:
        # print(data_misi)
        
        for misi in data_misi:
            status = "[V]" if misi['status_selesai'] == True else "[ ]"
            print(f"{status} | {misi['divisi']} - {misi['nama_misi']}")
except FileNotFoundError:
    print("Error: File papan_misi.json tidak ditemukan!")
