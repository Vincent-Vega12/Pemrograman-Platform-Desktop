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

# Membuat frame utama
main_frame = tk.Frame(
    master=window, 
    padx=20, 
    pady=20
)

main_frame.configure(bg="lavender")
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(1, weight=1)

# Judul menggunakan grid
label_judul = tk.Label(
    master=main_frame, 
    text="FORM BIODATA MAHASISWA", 
    font=("Arial", 16, "bold")
)

label_judul.configure(bg="#4B0082", fg="white")
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# Label Input Nama
label_nama = tk.Label(
    master=main_frame, 
    text="Nama Lengkap:", 
    font=("Arial", 12)
)

label_nama.grid(row=1, column=0, sticky="w", pady=5)

entry_nama = tk.Entry(
    master=main_frame, 
    width=30, 
    font=("Arial", 12)
)

entry_nama.grid(row=1, column=1, pady=5)

# Label Input NIM
label_nim = tk.Label(
    master=main_frame, 
    text="NIM:", 
    font=("Arial", 12)
)

label_nim.grid(
    row=2, 
    column=0, 
    sticky="w", 
    pady=5
)

entry_nim = tk.Entry(
    master=main_frame, 
    width=30, 
    font=("Arial", 12)
)

entry_nim.grid(row=2, column=1, pady=5)

# Input Jurusan
label_jurusan = tk.Label(
    master=main_frame, 
    text="Jurusan:", 
    font=("Arial", 12)
)

label_jurusan.grid(row=3, column=0, sticky="w", pady=5)

entry_jurusan = tk.Entry(
    master=main_frame, 
    width=30, 
    font=("Arial", 12)
)

entry_jurusan.grid(row=3, column=1, pady=5)

# Menjalankan main loop
window.mainloop()