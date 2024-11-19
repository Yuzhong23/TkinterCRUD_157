# Mengimpor modul untuk bekerja dengan SQLite dan Tkinter
import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database(): 
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor untuk eksekusi query
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit() # Menyimpan perubahan di database
    conn.close() # Menutup koneksi ke database

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    cursor.execute('SELECT * FROM nilai_siswa') # Menjalankan query untuk mengambil semua data
    rows = cursor.fetchall() # Mengambil semua hasil query
    conn.close()  # Menutup koneksi ke database
    return rows # Mengembalikan hasil query

# Fungsi untuk menyimpan data ke dalam database
def save_to_database(nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)) # Menyisipkan data
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi ke database
    
# Fungsi untuk memperbarui data siswa dalam database
def update_database(id, nama_siswa, biologi, fisika, inggris, prediksi_fakultas):
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama_siswa, biologi, fisika, inggris, prediksi_fakultas, id)) # Memperbarui data
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi ke database
    
# Fungsi untuk menghapus data siswa dari database
def delete_database(id):
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (id,)) # Menghapus data berdasarkan ID
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi ke database
    
# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calc_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi lebih tinggi dari fisika dan inggris
        return 'Kedokteran'  # Prediksi fakultas Kedokteran
    elif fisika > biologi and fisika > inggris:  # Jika nilai fisika lebih tinggi dari biologi dan inggris
        return 'Teknik'  # Prediksi fakultas Teknik
    elif inggris > biologi and inggris > fisika:  # Jika nilai inggris lebih tinggi dari biologi dan fisika
        return 'Bahasa'  # Prediksi fakultas Bahasa
    else:
        return 'Tidak Diketahui'  # Jika nilai tidak dominan, prediksi fakultas tidak diketahui


# Fungsi untuk menangani tombol submit (menyimpan data)
def submit():
    try:
        nama_siswa = nama_var.get()  # Mendapatkan input nama siswa
        biologi = int(biologi_var.get())  # Mendapatkan input nilai biologi dan mengubah ke integer
        fisika = int(fisika_var.get())  # Mendapatkan input nilai fisika dan mengubah ke integer
        inggris = int(inggris_var.get())  # Mendapatkan input nilai inggris dan mengubah ke integer
        
        if not nama_siswa:  # Jika nama siswa kosong, tampilkan pesan error
            raise Exception("Nama siswa harus diisi")
        
        prediksi = calc_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        
        save_to_database(nama_siswa, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database
        
        messagebox.showinfo("Sukses", "Data berhasil disimpan! \nPrediksi Fakultas: " + prediksi)  # Menampilkan pesan sukses
        clear_inputs()  # Mengosongkan inputan
        populate_table()  # Memperbarui tabel data setelah penyimpanan
    except ValueError as e:  # Jika terjadi kesalahan pada nilai input
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error
        
# Fungsi untuk menangani tombol update (memperbarui data)
def update():
    try:
        if not selected_id.get():  # Jika tidak ada ID yang dipilih
            raise Exception("Pilih data yang akan diupdate")
        
        id = int(selected_id.get())  # Mendapatkan ID yang dipilih
        nama_siswa = nama_var.get()  # Mendapatkan input nama siswa
        biologi = int(biologi_var.get())  # Mendapatkan input nilai biologi
        fisika = int(fisika_var.get())  # Mendapatkan input nilai fisika
        inggris = int(inggris_var.get())  # Mendapatkan input nilai inggris
        
        if not nama_siswa:  # Jika nama siswa kosong, tampilkan pesan error
            raise ValueError("Nama siswa harus diisi")
        
        prediksi = calc_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        
        update_database(selected_id.get(), nama_siswa, biologi, fisika, inggris, prediksi)  # Memperbarui data di database
        
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!\nPrediksi Fakultas: " + prediksi)  # Menampilkan pesan sukses
        clear_inputs()  # Mengosongkan inputan
        populate_table()  # Memperbarui tabel data setelah pembaruan
    except Exception as e:  # Menangani kesalahan lainnya
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error
        
# Fungsi untuk menangani tombol delete (menghapus data)
def delete():
    try:
        if not selected_id.get():  # Jika tidak ada ID yang dipilih
            raise Exception("Pilih data yang akan dihapus")
        
        id = int(selected_id.get())  # Mendapatkan ID yang dipilih
        delete_database(id)  # Menghapus data berdasarkan ID

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Mengosongkan inputan
        populate_table()  # Memperbarui tabel data setelah penghapusan
    except ValueError as e:  # Menangani kesalahan jika ID bukan angka
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error

# Fungsi untuk mengosongkan inputan setelah operasi
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama siswa
    biologi_var.set("")  # Mengosongkan input nilai biologi
    fisika_var.set("")  # Mengosongkan input nilai fisika
    inggris_var.set("")  # Mengosongkan input nilai inggris
    selected_id.set("")  # Mengosongkan ID yang dipilih

# Fungsi untuk memperbarui tabel dengan data terbaru dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua baris di tabel
        tree.delete(row)  # Menghapus setiap baris yang ada
    
    for row in fetch_data():  # Mengambil data terbaru dari database
        tree.insert("", "end", values=row)  # Menambahkan data baru ke tabel
        
# Fungsi mengisi input dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_data = tree.item(selected_item)['values']
        
        selected_id.set(selected_data[0])
        nama_var.set(selected_data[1])
        biologi_var.set(selected_data[2])
        fisika_var.set(selected_data[3])
        inggris_var.set(selected_data[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yg valid!")


# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")
# Membuat warna tampilan
root.configure(bg="lightgrey")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_id = StringVar()

# Element GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5,)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol Add, Update, dan Delete
Button(root, text="Add", command=submit).grid(row=4, column=0, padx=10, pady=5,)
Button(root, text="Update", command=update).grid(row=4, column=1, padx=10, pady=5)
Button(root, text="Delete", command=delete).grid(row=4, column=2, padx=10, pady=5)

# Tabel untuk menampilkan data
columns = ("ID", "Nama Siswa", "Biologi", "Fisika", "Bahasa Inggris", "Prediksi")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Bahasa Inggris", text="Bahasa Inggris")
tree.heading("Prediksi", text="Prediksi")
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menyatakan posisi teks di setiap kolom ke tengah
# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center")

tree.bind("<ButtonRelease-1>", fill_inputs_from_table)

root.mainloop()