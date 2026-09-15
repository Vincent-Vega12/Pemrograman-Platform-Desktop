# Mengimport library tkinter
import tkinter as tk

from tkinter import messagebox

def submit_data():
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return

    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    alamat = text_alamat.get("1.0", tk.END).strip()
    jenis_kelamin = var_jk.get()

    if not nama or not nim or not jurusan or not alamat:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("Data Tersimpan", hasil)

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela utama
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela utama
window.geometry("500x600")

# Mengaktifkan resize jendela
window.resizable(True, True)
window.minsize(500, 600)

#Mengatur warna latar belakang jendela utama
window.configure(bg="lavender")

# Membuat frame utama
main_frame = tk.Frame(
    master=window, 
    padx=20, 
    pady=20
)

main_frame.pack(fill=tk.BOTH, expand=True)

# Konfigurasi responsive layout
main_frame.grid_columnconfigure(1, weight=1)

# Variabel untuk radiobutton jenis kelamin
var_jk = tk.StringVar(value="Pria")

# Variabel untuk checkbox
var_setuju = tk.IntVar()

main_frame.columnconfigure(1, weight=1)
main_frame.configure(bg="lavender")

# Judul menggunakan grid
label_judul = tk.Label(
    master=main_frame, 
    text="FORM BIODATA MAHASISWA", 
    font=("Arial", 16, "bold"),
    foreground="Black",
)

label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# Frame khusus untuk input dengan border
frame_input = tk.Frame(
    master=main_frame, 
    relief=tk.GROOVE, 
    borderwidth=2, 
    padx=10, 
    pady=10
)

frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

# Input nama di dalam frame_input
label_nama = tk.Label(
    master=frame_input, 
    text="Nama Lengkap:", 
    font=("Arial", 12)
)

label_nama.grid(
    row=0, 
    column=0, 
    sticky="W", 
    pady=2
)

entry_nama = tk.Entry(
    master=frame_input, 
    width=30, 
    font=("Arial", 12)
)

entry_nama.grid(
    row=0,
    column=1,
    pady=2,
)

# Input NIM di dalam frame_input
label_nim = tk.Label(
    master=frame_input, 
    text="NIM:", 
    font=("Arial", 12)
)

label_nim.grid(
    row=1, 
    column=0, 
    sticky="W", pady=2
)

entry_nim = tk.Entry(
    master=frame_input, 
    width=30, 
    font=("Arial", 12)
)

entry_nim.grid(
    row=1, 
    column=1, 
    pady=2,
)

# Input Jurusan di dalam frame_input
label_jurusan = tk.Label(
    master=frame_input, 
    text="Jurusan:", 
    font=("Arial", 12)
)

label_jurusan.grid(
    row=2, 
    column=0, 
    sticky="W", 
    pady=2,
)

entry_jurusan = tk.Entry(
    master=frame_input, 
    width=30, 
    font=("Arial", 12)
)

entry_jurusan.grid(
    row=2, 
    column=1, 
    pady=2,
)

# Input alamat dengan Text widget
label_alamat = tk.Label(
    master=frame_input, 
    text="Alamat:", 
    font=("Arial", 12)
)

label_alamat.grid(
    row=3, 
    column=0, 
    sticky="NW", 
    pady=2,
)

# Frame untuk Text dan Scrollbar
frame_alamat = tk.Frame(
    master=frame_input, 
    relief=tk.SUNKEN, 
    borderwidth=1
)

# Scrollbar untuk alamat
scrollbar_alamat = tk.Scrollbar(
    master=frame_alamat
)

scrollbar_alamat.pack(
    side=tk.RIGHT, 
    fill=tk.Y
)

# Text widget untuk alamat
text_alamat = tk.Text(
    master=frame_alamat, 
    height=5, 
    width=28, 
    font=("Arial", 12)
)

text_alamat.pack(
    side=tk.LEFT, 
    fill=tk.BOTH, 
    expand=True
)

# Hubungkan scrollbar dengan text
scrollbar_alamat.config(
    command=text_alamat.yview
)

text_alamat.config(yscrollcommand=scrollbar_alamat.set)

frame_alamat.grid(
    row=3, 
    column=1, 
    pady=2
)

# Jenis kelamin di dalam frame_input
label_jk = tk.Label(
    master=frame_input, 
    text="Jenis Kelamin:", 
    font=("Arial", 12)
)

label_jk.grid(
    row=4, 
    column=0, 
    sticky="W", 
    pady=2
)

frame_jk = tk.Frame(master=frame_input)
frame_jk.grid(
    row=4, 
    column=1, 
    sticky="W"
)

radio_pria = tk.Radiobutton(
    master=frame_jk, 
    text="Pria", 
    variable=var_jk, 
    value="Pria"
)

radio_pria.pack(side=tk.LEFT)
radio_wanita = tk.Radiobutton(
    master=frame_jk, 
    text="Wanita", 
    variable=var_jk, 
    value="Wanita"
)

radio_wanita.pack(side=tk.LEFT)

# Checkbox di dalam frame_input
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10)
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

# Tombol submit
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit Biodata", 
    font=("Arial", 12, "bold"),
    command=submit_data
)

# Button submit (posisi disesuaikan)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

# Menjalankan main loop
window.mainloop()