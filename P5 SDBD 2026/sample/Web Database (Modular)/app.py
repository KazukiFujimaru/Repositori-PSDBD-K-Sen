from flask import Flask, render_template, request, redirect
import database # Mengimpor file mesin SQL kita

app = Flask(__name__)

@app.route('/')
def index():
    query = "SELECT * FROM tb_kontak"
    data = database.eksekusi_baca(query)
    return render_template('index.html', data_kontak=data)

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['input_nama']
    nohp = request.form['input_nohp']
    query = "INSERT INTO tb_kontak (nama, no_hp) VALUES (?, ?)"
    database.eksekusi_ubah(query, (nama, nohp))
    return redirect('/')

@app.route('/edit/<id_target>')
def edit_tampilan(id_target):
    query = "SELECT * FROM tb_kontak WHERE id_kontak = ?"
    # fetchone() diakali dengan mengambil indeks ke-[0] dari list hasil fetchall
    data = database.eksekusi_baca(query, (id_target,))[0] 
    return render_template('edit.html', data_lama=data)

@app.route('/edit_proses', methods=['POST'])
def edit_proses():
    id_target = request.form['input_id']
    nama_baru = request.form['input_nama']
    nohp_baru = request.form['input_nohp']
    query = "UPDATE tb_kontak SET nama = ?, no_hp = ? WHERE id_kontak = ?"
    database.eksekusi_ubah(query, (nama_baru, nohp_baru, id_target))
    return redirect('/')

@app.route('/hapus/<id_target>')
def hapus(id_target):
    query = "DELETE FROM tb_kontak WHERE id_kontak = ?"
    database.eksekusi_ubah(query, (id_target,))
    return redirect('/')

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)