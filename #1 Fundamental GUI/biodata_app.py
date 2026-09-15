# Mengimport library tkinter
import tkinter as tk

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela utama
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela utama
window.geometry("500x600")

#Mencegah jendela utama dapat diubah ukurannya
window.resizable(False, False)

#Mengatur warna latar belakang jendela utama
window.configure(bg="lavender")

# Membuat label untuk judul
label_judul = tk.Label (
    master=window,
    text="FORM BIODATA MAHASISWA",
    font=("Arial", 16, "bold"),
    foreground="White",
    background="#4B0082"
)

# Menampilkan label dengan pack
label_judul.pack(pady=20)

# Label untuk input nama
label_nama = tk.Label(
    master=window, 
    text="Nama Lengkap:", 
    font=("Arial", 12)
)

label_nama.pack(pady=5)

# Entry untuk input nama
entry_nama = tk.Entry(
    master=window, 
    font=("Arial", 12)
)

entry_nama.pack(pady=5)

# Label untuk input NIM
label_nim = tk.Label(
    master=window, 
    text="NIM:", 
    font=("Arial", 12)
)

label_nim.pack(pady=5)

# Entry untuk input NIM
entry_nim = tk.Entry(
    master=window, 
    font=("Arial", 12)
)

entry_nim.pack(pady=5)

# Label untuk input jurusan
label_jurusan = tk.Label(
    master=window, 
    text="Jurusan:", 
    font=("Arial", 12)
)

label_jurusan.pack(pady=5)

# Entry untuk input jurusan
entry_jurusan = tk.Entry(
    master=window, 
    font=("Arial", 12)
)

entry_jurusan.pack(pady=5)

# Menjalankan event loop
window.mainloop()