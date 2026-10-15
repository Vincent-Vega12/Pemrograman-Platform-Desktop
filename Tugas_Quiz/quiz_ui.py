import tkinter as tk
from tkinter import ttk


class QuizUI:
    TIMER_NORMAL = "#198754"
    TIMER_DANGER = "#DC3545"

    def __init__(self, parent, on_submit, on_skip):
        self.parent = parent
        self.on_submit = on_submit
        self.on_skip = on_skip

        self.selected_answer = tk.IntVar(value=-1)
        self.locked = False  # True setelah dijawab / skip / timeout

        self.time_left = 30
        self.timer_job = None
        self._timeout_callback = None

        self.animation_job = None
        self.animation_step = 0
        self.animation_colors = []

        self.build_quiz_widgets()

    # pembangunan widget
    def clear_parent(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def build_quiz_widgets(self):
        self.clear_parent()
        self.cancel_timer()
        self.cancel_animation()
        self.locked = False
        self.selected_answer.set(-1)

        # Header
        self.header = tk.Frame(self.parent, bg="#263B63", pady=13)
        self.header.pack(fill="x")

        tk.Label(
            self.header, text="QUIZ INTERAKTIF",
            font=("Arial", 19, "bold"), bg="#263B63", fg="white",
        ).pack()
        tk.Label(
            self.header, text="Uji Pengetahuanmu tentang Python",
            font=("Arial", 10), bg="#263B63", fg="#DCE6F7",
        ).pack(pady=(3, 0))

        # Area utama
        self.main_frame = tk.Frame(self.parent, bg="#F1F5F9", padx=28, pady=13)
        self.main_frame.pack(fill="both", expand=True)

        info_frame = tk.Frame(self.main_frame, bg="#F1F5F9")
        info_frame.pack(fill="x")

        self.question_label = tk.Label(
            info_frame, text="Soal 1/10",
            font=("Arial", 10, "bold"), bg="#F1F5F9", fg="#263B63",
        )
        self.question_label.pack(side="left")

        self.timer_label = tk.Label(
            info_frame, text="Waktu: 30 detik",
            font=("Arial", 10, "bold"), bg="#F1F5F9", fg=self.TIMER_NORMAL,
        )
        self.timer_label.pack(side="right")

        self.progress = ttk.Progressbar(
            self.main_frame, orient="horizontal",
            mode="determinate", maximum=10,
        )
        self.progress.pack(fill="x", pady=(7, 8))

        self.score_label = tk.Label(
            self.main_frame, text="Skor: 0 | Jawaban benar: 0",
            font=("Arial", 10), bg="#F1F5F9", fg="#475569",
        )
        self.score_label.pack(anchor="w", pady=(0, 8))

        self.question_text = tk.Label(
            self.main_frame, text="", font=("Arial", 12, "bold"),
            bg="white", fg="#1E293B", wraplength=600, justify="left",
            anchor="w", padx=12, pady=11,
        )
        self.question_text.pack(fill="x", pady=(0, 8))

        self.options_frame = tk.Frame(self.main_frame, bg="#F1F5F9")
        self.options_frame.pack(fill="x")

        self.radio_buttons = []
        for i in range(4):
            radio = tk.Radiobutton(
                self.options_frame, text="Pilihan jawaban",
                variable=self.selected_answer, value=i,
                font=("Arial", 10), bg="#F1F5F9",
                activebackground="#F1F5F9", fg="#334155",
                selectcolor="white", anchor="w", justify="left",
                wraplength=600, command=self._on_option_change,
            )
            radio.pack(fill="x", pady=1)
            self.radio_buttons.append(radio)

        self.feedback_label = tk.Label(
            self.main_frame, text="", font=("Arial", 10, "bold"),
            bg="#F1F5F9", fg="#334155", wraplength=620,
        )
        self.feedback_label.pack(pady=(4, 0))

        button_frame = tk.Frame(self.main_frame, bg="#F1F5F9")
        button_frame.pack(fill="x", pady=(5, 0))

        self.submit_button = tk.Button(
            button_frame, text="Submit Jawaban", command=self.on_submit,
            font=("Arial", 10, "bold"), bg="#315EAD", fg="white",
            activebackground="#244783", activeforeground="white",
            relief="flat", padx=16, pady=6, cursor="hand2",
        )
        self.submit_button.pack(side="left")

        self.skip_button = tk.Button(
            button_frame, text="Skip (Esc)", command=self.on_skip,
            font=("Arial", 10), bg="#E2E8F0", fg="#263B63",
            relief="flat", padx=16, pady=6, cursor="hand2",
        )
        self.skip_button.pack(side="right")

        self.footer = tk.Label(
            self.parent, text="Enter = Submit / Lanjut     |     Esc = Skip",
            font=("Arial", 9), bg="#E2E8F0", fg="#475569", pady=6,
        )
        self.footer.pack(fill="x", side="bottom")

    # ---------- render ----------
    def render_question(self, question, index, total, score, correct_count):
        self.cancel_timer()
        self.cancel_animation()
        self.locked = False
        self.selected_answer.set(-1)

        self.question_label.config(text=f"Soal {index + 1}/{total}")
        self.question_text.config(text=question["question"])
        self.score_label.config(
            text=f"Skor: {score} | Jawaban benar: {correct_count}"
        )
        self.progress["maximum"] = total
        self.progress["value"] = index

        self.feedback_label.config(
            text="", bg="#F1F5F9", fg="#334155", padx=0, pady=0
        )

        for i, option in enumerate(question["options"]):
            self.radio_buttons[i].config(
                text=option, state="normal", fg="#334155", bg="#F1F5F9"
            )

        self.submit_button.config(text="Submit Jawaban", state="normal")
        self.skip_button.config(state="normal")

    def update_score(self, score, correct_count):
        self.score_label.config(
            text=f"Skor: {score} | Jawaban benar: {correct_count}"
        )

    def lock_after_answer(self):
        self.locked = True
        self.progress["value"] = self.progress["value"] + 1
        for radio in self.radio_buttons:
            radio.config(state="disabled")
        self.submit_button.config(text="Lanjut", state="normal")
        self.skip_button.config(state="disabled")

    def get_selected(self):
        return self.selected_answer.get()

    def _on_option_change(self):
        # Hapus feedback sementara jika soal belum dikunci
        if self.locked:
            return
        self.cancel_animation()
        self.feedback_label.config(
            text="", bg="#F1F5F9", fg="#334155", padx=0, pady=0
        )

    # timer
    def start_timer(self, seconds, on_timeout):
        self.cancel_timer()
        self.time_left = seconds
        self._timeout_callback = on_timeout
        self._tick_timer()

    def _tick_timer(self):
        self.timer_label.config(
            text=f"Waktu: {self.time_left} detik",
            fg=self.TIMER_NORMAL if self.time_left > 10 else self.TIMER_DANGER,
        )
        if self.time_left <= 0:
            self.timer_job = None
            cb = self._timeout_callback
            self._timeout_callback = None
            if cb is not None:
                cb()
            return
        self.timer_job = self.parent.after(1000, self._countdown)

    def _countdown(self):
        self.timer_job = None
        if self.locked:
            return
        self.time_left -= 1
        self._tick_timer()

    def stop_timer(self):
        self.cancel_timer()
        self._timeout_callback = None

    def cancel_timer(self):
        if self.timer_job is not None:
            try:
                self.parent.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    # feedback + animasi
    def show_correct(self, text="BENAR! +10 poin"):
        self._animate(text, "#198754", "#D1FAE5")

    def show_wrong(self, correct_option):
        self._animate(
            f"SALAH! Jawaban benar: {correct_option}", "#DC2626", "#FEE2E2"
        )

    def show_skipped(self):
        self.cancel_animation()
        self.feedback_label.config(
            text="Soal dilewati. Tidak ada poin yang diperoleh.",
            fg="#92400E", bg="#FEF3C7", padx=8, pady=4,
        )

    def show_timeout(self):
        self.cancel_animation()
        self.feedback_label.config(
            text="WAKTU HABIS! Soal ini tidak mendapat poin.",
            fg="#DC2626", bg="#FEE2E2", padx=8, pady=4,
        )

    def _animate(self, text, color, background):
        self.cancel_animation()
        self.feedback_label.config(
            text=text, fg=color, bg=background, padx=8, pady=4
        )
        self.animation_colors = [background, "#F1F5F9", background, "#F1F5F9"]
        self.animation_step = 0
        self._animate_step()

    def _animate_step(self):
        if self.animation_step >= len(self.animation_colors):
            self.feedback_label.config(bg="#F1F5F9")
            self.animation_job = None
            return
        color = self.animation_colors[self.animation_step]
        self.feedback_label.config(bg=color)
        self.animation_step += 1
        self.animation_job = self.parent.after(150, self._animate_step)

    def cancel_animation(self):
        if self.animation_job is not None:
            try:
                self.parent.after_cancel(self.animation_job)
            except tk.TclError:
                pass
            self.animation_job = None

    def cleanup(self):
        self.stop_timer()
        self.cancel_animation()

    # layar hasil 
    def show_result(self, result, on_restart):
        self.cleanup()
        self.clear_parent()

        result_frame = tk.Frame(self.parent, bg="#F1F5F9", padx=30, pady=20)
        result_frame.pack(fill="both", expand=True)

        tk.Label(
            result_frame, text="QUIZ SELESAI!",
            font=("Arial", 23, "bold"), bg="#F1F5F9", fg="#263B63",
        ).pack(pady=(20, 15))

        tk.Label(
            result_frame, text=str(result["score"]),
            font=("Arial", 42, "bold"), bg="#F1F5F9", fg="#315EAD",
        ).pack()

        tk.Label(
            result_frame, text="TOTAL SKOR",
            font=("Arial", 11, "bold"), bg="#F1F5F9", fg="#64748B",
        ).pack()

        tk.Label(
            result_frame,
            text=(
                f"Jawaban benar: {result['correct']}/{result['total']}\n"
                f"Persentase: {result['percentage']:.0f}%\n\n"
                f"{result['message']}"
            ),
            font=("Arial", 12), justify="center",
            bg="#F1F5F9", fg="#334155",
        ).pack(pady=18)

        tk.Button(
            result_frame, text="Main Lagi", command=on_restart,
            font=("Arial", 11, "bold"), bg="#315EAD", fg="white",
            activebackground="#244783", activeforeground="white",
            relief="flat", padx=25, pady=9, cursor="hand2",
        ).pack()
