
import tkinter as tk
from tkinter import ttk


class CustomStyleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Styling dengan ttk")
        self.root.geometry("700x500")
        self.root.configure(bg="#2c3e50")

        # Inisialisasi style
        self.style = ttk.Style()

        # Menggunakan theme clam agar custom warna lebih terlihat
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self._setup_custom_styles()
        self._buat_interface()

    def _setup_custom_styles(self):
        # Custom style untuk button
        self.style.configure(
            "Custom.TButton",
            background="#3498db",
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            padding=(20, 10)
        )

        self.style.map(
            "Custom.TButton",
            background=[
                ("active", "#2980b9"),
                ("pressed", "#21618c")
            ]
        )

        # Custom style untuk entry
        self.style.configure(
            "Custom.TEntry",
            fieldbackground="#ecf0f1",
            borderwidth=2,
            insertcolor="#2c3e50",
            padding=(10, 8)
        )

        self.style.map(
            "Custom.TEntry",
            bordercolor=[("focus", "#3498db")]
        )

        # Custom style untuk label
        self.style.configure(
            "Title.TLabel",
            background="#2c3e50",
            foreground="#ecf0f1",
            font=("Arial", 18, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background="#2c3e50",
            foreground="#bdc3c7",
            font=("Arial", 12)
        )

    def _buat_interface(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 30))

        ttk.Label(
            header_frame,
            text="Custom Styling Demo",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            header_frame,
            text="Aplikasi dengan styling kustom menggunakan ttk.Style",
            style="Subtitle.TLabel"
        ).pack(pady=(5, 0))

        # Form section
        form_frame = ttk.LabelFrame(
            main_frame,
            text="Form Input",
            padding="20"
        )
        form_frame.pack(fill="x", pady=(0, 20))

        # Nama input
        ttk.Label(
            form_frame,
            text="Nama Lengkap:"
        ).pack(anchor="w", pady=(0, 5))

        self.nama_entry = ttk.Entry(
            form_frame,
            style="Custom.TEntry",
            width=40
        )
        self.nama_entry.pack(fill="x", pady=(0, 15))

        # Email input
        ttk.Label(
            form_frame,
            text="Email:"
        ).pack(anchor="w", pady=(0, 5))

        self.email_entry = ttk.Entry(
            form_frame,
            style="Custom.TEntry",
            width=40
        )
        self.email_entry.pack(fill="x", pady=(0, 15))

        # Button section
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            button_frame,
            text="Submit Data",
            style="Custom.TButton",
            command=self.submit_data
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            button_frame,
            text="Reset Form",
            style="Custom.TButton",
            command=self.reset_form
        ).pack(side="left")

        # Result section
        self.result_frame = ttk.LabelFrame(
            main_frame,
            text="Hasil Input",
            padding="20"
        )
        self.result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            self.result_frame,
            height=8,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Consolas", 10)
        )
        self.result_text.pack(fill="both", expand=True)

    def submit_data(self):
        nama = self.nama_entry.get()
        email = self.email_entry.get()

        if nama and email:
            result = (
                f"Data berhasil disubmit:\n"
                f"Nama: {nama}\n"
                f"Email: {email}\n"
                + "=" * 40 + "\n"
            )

            self.result_text.insert("end", result)
            self.result_text.see("end")

        else:
            self.result_text.insert(
                "end",
                "Error: Semua field harus diisi!\n"
                + "=" * 40 + "\n"
            )
            self.result_text.see("end")

    def reset_form(self):
        self.nama_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.result_text.delete("1.0", "end")

    def run(self):
        self.root.mainloop()


# Jalankan aplikasi
if __name__ == "__main__":
    app = CustomStyleApp()
    app.run()
