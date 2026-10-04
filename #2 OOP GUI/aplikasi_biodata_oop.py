import tkinter as tk
from tkinter import messagebox

# Membuat Kelas Utama Aplikasi yang Mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        # Memanggil Constructor dari kelas induk (tk.Tk)
        super().__init__()

        # Mengkonfirmasi window utama
        self.title("Aplikasi Biodata (Versi OOP)")
        self.geometry("500x600")
        self.resizable(True, True)
        self.configure(bg="lavender")

        # Variabel Kontrol Tkinter
        # Variabel-variabel berikut sekarang menjadi atribut dari instance kelas
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # FRAME UTAMA
        # Frame utama juga menjadi atribut
        self.main_frame = tk.Frame(
            master=self,
            padx=20,
            pady=20
        )

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.configure(bg="lavender")

        #  Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # Membuat dan Menempatkan Widget
        # Judul
        self.label_judul = tk.Label(
            master=self.main_frame,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )

        # Frame Khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.main_frame,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10
        )

        self.frame_input.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="EW"
        )

        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input,
            text="Nama Lengkap:",
            font=("Arial", 12)
        )
        self.label_nama.grid(
            row=0,
            column=0,
            sticky="W",
            pady=2
        )

        self.entry_nama = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nama
        )
        self.entry_nama.grid(
            row=0,
            column=1,
            pady=2
        )

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input, 
            text="NIM:", 
            font=("Arial", 12)
        )
        self.label_nim.grid(
            row=1,
            column=0,
            sticky="W",
            pady=2
        )
        self.entry_nim = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_nim
        )
        self.entry_nim.grid(
            row=1,
            column=1,
            pady=2
        )

        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input, 
            text="Jurusan:", 
            font=("Arial", 12)
        )
        self.label_jurusan.grid(
            row=2,
            column=0,
            sticky="W",
            pady=2
        )
        self.entry_jurusan = tk.Entry(
            master=self.frame_input, 
            width=30, 
            font=("Arial", 12), 
            textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(
            row=2,
            column=1,
            pady=2
        )

        # Input Alamat dengan Text Widget
        self.label_alamat = tk.Label(
            master=self.frame_input, 
            text="Alamat:", 
            font=("Arial", 12)
        )
        self.label_alamat.grid(
            row=3,
            column=0,
            sticky="NW",
            pady=2
        )

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(
            master=self.frame_input, 
            relief=tk.SUNKEN, 
            borderwidth=1
        )

        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(
            master=self.frame_alamat, 
            height=5, 
            width=28, 
            font=("Arial", 12)
        )
        self.text_alamat.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)
        self.frame_alamat.grid(
            row=3,
            column=1,
            pady=2
        )

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input, 
            text="Jenis Kelamin:", 
            font=("Arial", 12)
        )
        self.label_jk.grid(
            row=4,
            column=0,
            sticky="W",
            pady=2
        )

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(
            row=4,
            column=1,
            sticky="W"
        )

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk, 
            text="Pria", 
            variable=self.var_jk, 
            value="Pria"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk, 
            text="Wanita", 
            variable=self.var_jk, 
            value="Wanita"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )
        self.check_setuju.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10,
            sticky="W"
        )

        self.frame_input.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="EW"
        )

        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.main_frame, 
            text="Submit Biodata", 
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=20,
            sticky="EW"
        )

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.main_frame, 
            text="", 
            font=("Arial", 12, "italic"), 
            justify=tk.LEFT
        )
        self.label_hasil.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="W",
            padx=10
        )

    def submit_data(self):
        # Cek Checkbox
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        # Ambil data dari form
        nama = self.entry_nama.get()
        nim = self.entry_nim.get()
        jurusan = self.entry_jurusan.get()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        # Cek field kosong
        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        # Tampilkan hasil
        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)

        # Tampilkan hasil di label
        self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()
        
        # (Di sini kita akan meletakkan semua kode GUI nantinya)
# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
     # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()