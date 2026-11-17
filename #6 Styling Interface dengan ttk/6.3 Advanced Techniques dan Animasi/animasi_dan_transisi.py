import tkinter as tk
from tkinter import ttk


class AnimatedApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Animasi dan Transisi dengan ttk")
        self.root.geometry("800x650")
        self.root.minsize(600, 500)
        self.root.configure(bg="#1a1a1a")

        # Variabel animasi
        self.progress_value = 0
        self.progress_job = None
        self.slide_job = None
        self.fade_job = None
        self.panel_x = -300
        self.fade_visible = True
        self.fade_step = 0

        self._setup_styles()
        self._buat_interface()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Dark.TFrame",
            background="#2d2d2d"
        )
        self.style.configure(
            "Dark.TLabel",
            background="#2d2d2d",
            foreground="#ffffff",
            font=("Arial", 11)
        )
        self.style.configure(
            "Title.TLabel",
            background="#2d2d2d",
            foreground="#00ff88",
            font=("Arial", 16, "bold")
        )
        self.style.configure(
            "Animated.TButton",
            background="#00cc77",
            foreground="#1a1a1a",
            padding=(15, 8),
            font=("Arial", 10, "bold")
        )
        self.style.map(
            "Animated.TButton",
            background=[("active", "#00e68a"), ("pressed", "#009954")]
        )
        self.style.configure(
            "TProgressbar",
            troughcolor="#444444",
            background="#00ff88",
            thickness=18
        )

    def _buat_interface(self):
        self.main_frame = ttk.Frame(self.root, style="Dark.TFrame", padding=20)
        self.main_frame.pack(fill="both", expand=True)

        ttk.Label(
            self.main_frame,
            text="🎬 Animation Demo",
            style="Title.TLabel"
        ).pack(pady=(0, 20))

        # Progress animation
        self.progress_frame = ttk.LabelFrame(
            self.main_frame, text="Progress Animation", padding=15
        )
        self.progress_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            self.progress_frame,
            text="Animated Progress Bar:"
        ).pack(anchor="w", pady=(0, 8))

        self.progress_bar = ttk.Progressbar(
            self.progress_frame, mode="determinate", maximum=100
        )
        self.progress_bar.pack(fill="x", pady=(0, 12))

        progress_controls = ttk.Frame(self.progress_frame)
        progress_controls.pack(fill="x")

        ttk.Button(
            progress_controls, text="Start Animation",
            style="Animated.TButton", command=self.start_progress_animation
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            progress_controls, text="Stop Animation",
            style="Animated.TButton", command=self.stop_animation
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            progress_controls, text="Reset",
            style="Animated.TButton", command=self.reset_progress
        ).pack(side="left")

        # Sliding panel
        self.slide_frame = ttk.LabelFrame(
            self.main_frame, text="Sliding Panel", padding=15
        )
        self.slide_frame.pack(fill="x", pady=(0, 15))

        self.slide_container = ttk.Frame(
            self.slide_frame, style="Dark.TFrame", height=130
        )
        self.slide_container.pack(fill="x", pady=(0, 12))
        self.slide_container.pack_propagate(False)

        self.sliding_panel = ttk.Frame(
            self.slide_container, style="Dark.TFrame"
        )
        self.sliding_panel.place(x=-300, y=0, width=300, height=130)

        panel_content = ttk.Frame(self.sliding_panel, style="Dark.TFrame")
        panel_content.pack(fill="both", expand=True, padx=15, pady=15)

        ttk.Label(
            panel_content, text="🎯 Sliding Panel Content",
            style="Title.TLabel"
        ).pack()
        ttk.Label(
            panel_content,
            text="Panel bergerak masuk dan keluar secara bertahap.",
            style="Dark.TLabel"
        ).pack(pady=(8, 0))

        slide_controls = ttk.Frame(self.slide_frame)
        slide_controls.pack(fill="x")

        ttk.Button(
            slide_controls, text="Slide In",
            style="Animated.TButton", command=self.slide_in
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            slide_controls, text="Slide Out",
            style="Animated.TButton", command=self.slide_out
        ).pack(side="left")

        # Fade-like transition
        self.fade_frame = ttk.LabelFrame(
            self.main_frame, text="Fade Animation", padding=15
        )
        self.fade_frame.pack(fill="both", expand=True)

        self.fade_content = ttk.Frame(self.fade_frame, style="Dark.TFrame")
        self.fade_content.pack(fill="both", expand=True, pady=(0, 12))

        ttk.Label(
            self.fade_content, text="✨ Fade Content",
            style="Title.TLabel"
        ).pack(pady=15)
        ttk.Label(
            self.fade_content,
            text="Efek fade disimulasikan dengan menyembunyikan dan menampilkan konten.",
            style="Dark.TLabel",
            wraplength=600
        ).pack()

        fade_controls = ttk.Frame(self.fade_frame)
        fade_controls.pack(fill="x")

        ttk.Button(
            fade_controls, text="Fade Out",
            style="Animated.TButton", command=self.fade_out
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            fade_controls, text="Fade In",
            style="Animated.TButton", command=self.fade_in
        ).pack(side="left")

    # Progress bar menggunakan after agar update terjadi di thread Tkinter
    def start_progress_animation(self):
        if self.progress_job is None and self.progress_value < 100:
            self._animate_progress()

    def _animate_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar["value"] = self.progress_value
            self.progress_job = self.root.after(40, self._animate_progress)
        else:
            self.progress_job = None

    def stop_animation(self):
        if self.progress_job is not None:
            self.root.after_cancel(self.progress_job)
            self.progress_job = None

    def reset_progress(self):
        self.stop_animation()
        self.progress_value = 0
        self.progress_bar["value"] = 0

    # Sliding panel
    def slide_in(self):
        self._stop_slide()
        self._animate_slide(0)

    def slide_out(self):
        self._stop_slide()
        self._animate_slide(-300)

    def _stop_slide(self):
        if self.slide_job is not None:
            self.root.after_cancel(self.slide_job)
            self.slide_job = None

    def _animate_slide(self, target_x):
        difference = target_x - self.panel_x
        if abs(difference) <= 5:
            self.panel_x = target_x
            self.sliding_panel.place(
                x=self.panel_x, y=0, width=300, height=130
            )
            self.slide_job = None
            return

        self.panel_x += 5 if difference > 0 else -5
        self.sliding_panel.place(
            x=self.panel_x, y=0, width=300, height=130
        )
        self.slide_job = self.root.after(
            15, lambda: self._animate_slide(target_x)
        )

    # Tkinter tidak menyediakan transparansi per-widget secara langsung.
    # Karena itu, efek fade dibuat sebagai transisi tampil/sembunyi bertahap.
    def fade_out(self):
        if self.fade_job is not None:
            self.root.after_cancel(self.fade_job)
            self.fade_job = None
        if self.fade_visible:
            self.fade_step = 0
            self._animate_fade_out()

    def _animate_fade_out(self):
        self.fade_step += 1
        if self.fade_step >= 10:
            self.fade_content.pack_forget()
            self.fade_visible = False
            self.fade_job = None
            return

        self.fade_job = self.root.after(35, self._animate_fade_out)

    def fade_in(self):
        if self.fade_job is not None:
            self.root.after_cancel(self.fade_job)
            self.fade_job = None
        if not self.fade_visible:
            self.fade_content.pack(
                fill="both", expand=True, pady=(0, 12),
                before=self.fade_frame.winfo_children()[-1]
            )
            self.fade_visible = True
            self.fade_step = 0
            self._animate_fade_in()

    def _animate_fade_in(self):
        self.fade_step += 1
        if self.fade_step >= 10:
            self.fade_job = None
            return
        self.fade_job = self.root.after(35, self._animate_fade_in)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AnimatedApp()
    app.run()
