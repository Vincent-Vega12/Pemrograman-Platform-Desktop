"""Model / state management untuk Quiz Interaktif.

Murni logika Python, tanpa Tkinter agar mudah di-test dan diperbaiki.
"""
import random


class QuizManager:
    def __init__(self, questions=None):
        self.questions = questions if questions is not None else self.get_default_questions()
        self.current_question = 0
        self.score = 0
        self.correct_count = 0

    @staticmethod
    def get_default_questions():
        return [
            {
                "question": "Apa itu event-driven programming?",
                "options": [
                    "Program yang berjalan berurutan",
                    "Program yang merespons kejadian",
                    "Program tanpa GUI",
                    "Program berbasis web",
                ],
                "correct": 1,
            },
            {
                "question": "Library Python untuk membuat GUI adalah ...",
                "options": ["NumPy", "Pandas", "Tkinter", "Flask"],
                "correct": 2,
            },
            {
                "question": "Apa fungsi method __init__()?",
                "options": [
                    "Menghapus objek",
                    "Menginisialisasi objek",
                    "Menutup program",
                    "Mengulang program",
                ],
                "correct": 1,
            },
            {
                "question": "Widget untuk memilih satu jawaban adalah ...",
                "options": ["Label", "Entry", "Radiobutton", "Frame"],
                "correct": 2,
            },
            {
                "question": "Apa fungsi method after() pada Tkinter?",
                "options": [
                    "Menjalankan fungsi setelah jeda waktu",
                    "Menghapus widget",
                    "Menutup aplikasi",
                    "Menyimpan file",
                ],
                "correct": 0,
            },
            {
                "question": "Apa kegunaan tk.IntVar()?",
                "options": [
                    "Menyimpan nilai integer yang terhubung ke widget",
                    "Membuat gambar",
                    "Mengatur ukuran jendela",
                    "Menghentikan program",
                ],
                "correct": 0,
            },
            {
                "question": "Event keyboard untuk tombol Enter adalah ...",
                "options": ["<Escape>", "<Return>", "<Space>", "<Tab>"],
                "correct": 1,
            },
            {
                "question": "Apa fungsi try dan except dalam Python?",
                "options": [
                    "Membuat tampilan",
                    "Menangani kesalahan",
                    "Mengurutkan data",
                    "Mengubah warna",
                ],
                "correct": 1,
            },
            {
                "question": "Apa fungsi ttk.Progressbar?",
                "options": [
                    "Menampilkan kemajuan proses",
                    "Memilih jawaban",
                    "Membuat variabel",
                    "Menampilkan pesan error",
                ],
                "correct": 0,
            },
            {
                "question": "Apa yang dimaksud state management?",
                "options": [
                    "Mengatur warna aplikasi",
                    "Mengelola kondisi dan data aplikasi",
                    "Menghapus kode",
                    "Mengatur nama file",
                ],
                "correct": 1,
            },
        ]

    def shuffle(self):
        random.shuffle(self.questions)

    def get_total(self):
        return len(self.questions)

    def get_current(self):
        if 0 <= self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def is_finished(self):
        return self.current_question >= len(self.questions)

    def check_answer(self, selected_idx):
        """Cek jawaban, update skor. Return (is_correct, correct_option_text)."""
        question = self.get_current()
        if question is None:
            return False, ""
        correct_idx = question["correct"]
        correct_text = question["options"][correct_idx]
        if selected_idx == correct_idx:
            self.score += 10
            self.correct_count += 1
            return True, correct_text
        return False, correct_text

    def next(self):
        self.current_question += 1
        return not self.is_finished()

    def get_result(self):
        total = len(self.questions)
        percentage = (self.correct_count / total * 100) if total else 0
        if percentage >= 80:
            message = "Hebat! Pemahamanmu sangat baik."
        elif percentage >= 60:
            message = "Bagus! Terus tingkatkan kemampuanmu."
        else:
            message = "Tetap semangat dan coba belajar lagi!"
        return {
            "score": self.score,
            "correct": self.correct_count,
            "total": total,
            "percentage": percentage,
            "message": message,
        }

    def reset(self):
        self.current_question = 0
        self.score = 0
        self.correct_count = 0
        self.shuffle()
