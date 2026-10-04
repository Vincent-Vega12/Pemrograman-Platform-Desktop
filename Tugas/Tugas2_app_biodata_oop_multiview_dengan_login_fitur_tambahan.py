import tkinter as tk
from tkinter import messagebox
import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat Kelas Utama Aplikasi yang Mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        # Memanggil Constructor dari kelas induk (tk.Tk)
        super().__init__()

        # Mengkonfirmasi window utama
        self.title("Aplikasi Biodata (Versi OOP)")
        self.geometry("600x700")
        self.resizable(True, True)
        self.configure(bg="lavender")

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
            "ridwans": "24106050021"
        }

        # Warna setiap user
        self.user_colors = {
            "admin": "#DDEBFF",
            "user1": "#E8F5E9",
            "mahasiswa": "#FFF3CD",
            "ridwans": "#FCE4EC"
        }

        # Status login
        self.current_user = None

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Membuat tampilan biodata
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        # Log aplikasi start
        logging.info("Aplikasi dimulai")

    def _ubah_warna_user(self):
        warna = self.user_colors.get(
            self.current_user,
            "#E8DFF5"
        )

        self.configure(bg=warna)
        self.frame_biodata.configure(bg=warna)
        self.label_judul.configure(bg=warna)
        self.label_hasil.configure(bg=warna)

    # Tampilan Login
    def _buat_tampilan_login(self):
        self.var_remember = tk.IntVar(value=0)

        self.frame_login = tk.Frame(master=self, padx=20, pady=100)

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Input Username
        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)

        self.entry_username = tk.Entry(
            self.frame_login,
            font=("Arial", 12)
        )

        self.entry_username.grid(
            row=1,
            column=1,
            pady=5,
            sticky="EW"
        )

        # Input Password
        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12)
        ).grid(
            row=2,
            column=0,
            sticky="W",
            pady=5
        )

        self.entry_password = tk.Entry(
            self.frame_login, 
            font=("Arial", 12), 
            show="*"
        )
        self.entry_password.grid(
            row=2,
            column=1,
            pady=5,
            sticky="EW"
        )

        self.btn_show_password = tk.Button(
            self.frame_login,
            text="Show",
            command=self._toggle_password
        )

        self.btn_show_password.grid(
            row=2,
            column=2
        )

        self.check_remember = tk.Checkbutton(
        self.frame_login,
        text="Remember Me",
        variable=self.var_remember
        )

        self.check_remember.grid(
        row=3,
        column=0,
        columnspan=2,
        sticky="W",
        pady=5
        )

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login, 
        text="Login", 
        font=("Arial", 12, "bold"),
        command=self._coba_login
        )

        self.btn_login.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=20,
            sticky="EW"
        )

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456) \nridwans (password: 24106050021)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )

    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _coba_login(self):
        """Method untuk memproses attempt login"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return
        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")
            self._ubah_warna_user()
            self._reset_form_biodata()
            self._update_title_with_user()
            # BUAT MENU SETELAH LOGIN
            self._buat_menu()
            self._pindah_ke(self.frame_biodata)
            # Simpan username jika Remember Me dicentang
            if self.var_remember.get() == 1:
                self.remembered_username = username
            else:
                self.remembered_username = ""

            # Bersihkan field login setelah berhasil
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah.")
            # Bersihkan password dan focus ke username
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")

    def _logout(self):
        """Method untuk logout dan kembali ke halaman login"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Hapus menu
            self._hapus_menu()
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            # Tampilkan kembali username yang diingat
            if self.var_remember.get() == 1 and hasattr(self, "remembered_username"):
                self.entry_username.insert(0, self.remembered_username)
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    def _buat_menu(self):
            """Membuat menu bar untuk aplikasi"""
            menu_bar = tk.Menu(master=self)
            self.config(menu=menu_bar)
    
            file_menu = tk.Menu(master=menu_bar,tearoff=0)
            file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
            file_menu.add_separator()
            file_menu.add_command(label="Logout", command=self._logout)
            file_menu.add_separator()
            file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)
    
            menu_bar.add_cascade(label="File", menu=file_menu)

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Tampilkan hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            # Log successful data submission
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan saat memproses data:\n{str(e)}"
            )
            logging.error(
                f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror(
                "Error",
                f"Terjadi kesalahan saat memproses data:\n{str(e)}"
            )

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

    # Migrasi dari init
    def _buat_tampilan_biodata(self):
        # Variabel Kontrol Tkinter
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # FRAME BIODATA
        self.frame_biodata = tk.Frame(
            master=self,
            padx=20,
            pady=20,
            bg="lavender"
        )

        self.frame_biodata.columnconfigure(1, weight=1)

        # JUDUL
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold")
        )

        self.label_judul.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )

        # FRAME INPUT
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
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

        # INPUT NAMA
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

        # INPUT NIM
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

        # INPUT JURUSAN
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

    # INPUT ALAMAT
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

        # Scrollbar
        self.scrollbar_alamat = tk.Scrollbar(
            master=self.frame_alamat
        )

        self.scrollbar_alamat.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # Text widget
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

        # Hubungkan scrollbar dengan Text
        self.scrollbar_alamat.config(
            command=self.text_alamat.yview
        )

        self.text_alamat.config(
            yscrollcommand=self.scrollbar_alamat.set
        )

        self.frame_alamat.grid(
            row=3,
            column=1,
            pady=2
        )

        # JENIS KELAMIN
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

        self.frame_jk = tk.Frame(
            master=self.frame_input
        )

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

        self.radio_pria.pack(
            side=tk.LEFT
        )

        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita"
        )

        self.radio_wanita.pack(
            side=tk.LEFT
        )

        # CHECKBOX PERSETUJUAN
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
            pady=10,
            sticky="W"
        )

        # TOMBOL SUBMIT
        self.btn_submit = tk.Button(
            master=self.frame_biodata,
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

        # RESET FORM BUTTON
        self.btn_reset = tk.Button(
            self.frame_input,
            text="↻ Reset",
            font=("Arial", 10),
            command=self._reset_form_biodata
        )

        self.btn_reset.grid(
            row=5,
            column=1,
            padx=25,
            pady=10,
            sticky="E"
        )

        # Event hover
        self.btn_submit.bind(
            "<Enter>",
            self.on_enter
        )

        self.btn_submit.bind(
            "<Leave>",
            self.on_leave
        )

        # KEYBOARD SHORTCUTS
        self.entry_nama.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_nim.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_jurusan.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.text_alamat.bind(
            "<Return>",
            self.submit_shortcut
        )

        # LABEL HASIL
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Arial", 11, "italic"),
            justify=tk.LEFT,
        )

        self.label_hasil.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="W",
            padx=10
        )

        # Membuat menu
        self._buat_menu()

    def _hapus_menu(self):
        """Menghapus menu bar dari window."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def simpan_hasil(self):
        """Simpan Hasil Biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidaka ada data untuk disimpan. Mohonsubmit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def _toggle_password(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.config(show="")
            self.btn_show_password.config(text="Hide")
        else:
            self.entry_password.config(show="*")
            self.btn_show_password.config(text="Show")

        # (Di sini kita akan meletakkan semua kode GUI nantinya)
# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
     # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()