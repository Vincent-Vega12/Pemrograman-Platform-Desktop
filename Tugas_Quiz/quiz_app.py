"""menghubungkan QuizManager + QuizUI."""
import tkinter as tk
from tkinter import messagebox

from quiz_manager import QuizManager
from quiz_ui import QuizUI


class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        self.window.configure(bg="#F1F5F9")

        self.manager = QuizManager()
        self.manager.shuffle()

        self.ui = QuizUI(
            self.window,
            on_submit=self.submit_answer,
            on_skip=self.skip_question,
        )

        self.window.bind("<Return>", self.handle_enter)
        self.window.bind("<Escape>", self.handle_escape)
        self.window.protocol("WM_DELETE_WINDOW", self.close_app)

        self.load_question()

    
    def buat_interface(self):
        self.ui.build_quiz_widgets()

    def load_question(self):
        if self.manager.is_finished():
            self.show_result()
            return
        q = self.manager.get_current()
        self.ui.render_question(
            q,
            self.manager.current_question,
            self.manager.get_total(),
            self.manager.score,
            self.manager.correct_count,
        )
        self.start_timer()

    def start_timer(self):
        self.ui.start_timer(30, self.timeout_question)

    def submit_answer(self):
        if self.manager.is_finished():
            return
        # Tombol berubah jadi "Lanjut" setelah dijawab
        if self.ui.locked:
            self.next_question()
            return
        selected = self.ui.get_selected()
        if selected == -1:
            messagebox.showwarning(
                "Peringatan",
                "Pilih jawaban terlebih dahulu!",
                parent=self.window,
            )
            return
        is_correct, correct_text = self.manager.check_answer(selected)
        self.ui.stop_timer()
        if is_correct:
            self.ui.show_correct()
        else:
            self.ui.show_wrong(correct_text)
        self.ui.update_score(self.manager.score, self.manager.correct_count)
        self.ui.lock_after_answer()

    def show_result(self):
        result = self.manager.get_result()
        self.ui.show_result(result, self.restart_quiz)

    def jalankan(self):
        self.window.mainloop()

    
    def next_question(self):
        if not self.ui.locked or self.manager.is_finished():
            return
        self.manager.next()
        self.load_question()

    def skip_question(self):
        if self.manager.is_finished() or self.ui.locked:
            return
        self.ui.stop_timer()
        self.ui.show_skipped()
        self.ui.lock_after_answer()

    def timeout_question(self):
        if self.manager.is_finished() or self.ui.locked:
            return
        self.ui.show_timeout()
        self.ui.lock_after_answer()

    def restart_quiz(self):
        self.manager.reset()
        self.ui.build_quiz_widgets()
        self.load_question()

    def handle_enter(self, event=None):
        if self.manager.is_finished():
            return "break"
        if self.ui.locked:
            self.next_question()
        else:
            self.submit_answer()
        return "break"

    def handle_escape(self, event=None):
        if self.manager.is_finished():
            return "break"
        self.skip_question()
        return "break"

    def close_app(self):
        self.ui.cleanup()
        self.window.destroy()
