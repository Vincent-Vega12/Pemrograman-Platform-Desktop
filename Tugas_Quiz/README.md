# Quiz Interaktif — Tugas Pemrograman Platform Desktop

Aplikasi desktop **Quiz Interaktif** berbasis Python Tkinter. Menggabungkan konsep event-driven programming, timer, validasi, state management, dan animasi feedback dalam arsitektur OOP multi-file agar mudah dikustomisasi.

## Fitur

- 10 soal pilihan ganda dengan `Radiobutton`
- Timer countdown 30 detik per soal (otomatis timeout jika habis)
- Real-time score tracking + `ttk.Progressbar`
- Validasi jawaban sebelum lanjut (wajib pilih dulu)
- Animasi feedback benar / salah / skip / timeout
- Keyboard shortcut: `Enter` submit / lanjut, `Esc` skip
- State management terpusat (posisi, skor, history)
- Layar hasil: total skor, persentase, pesan, tombol Main Lagi
- Restart quiz dengan soal teracak ulang

## Struktur Proyek

```text
Tugas_Quiz/
├── main.py          # Entry point
├── quiz_app.py      # Controller / orkestrator (QuizApp)
├── quiz_manager.py  # Model + state + penilaian (QuizManager)
├── quiz_ui.py       # View Tkinter + timer + animasi (QuizUI)
└── README.md
```

- `quiz_manager.py`: data 10 soal, `shuffle()`, `check_answer()`, `next()`, `get_result()`, `reset()`. Murni Python, tanpa Tkinter.
- `quiz_ui.py`: semua widget, `after()` timer, animasi feedback, layar hasil. Tidak menilai jawaban.
- `quiz_app.py`: menyambungkan keduanya, binding keyboard, alur submit → skip → timeout → next → result.
- `main.py`: menjalankan `QuizApp().jalankan()`.

## Cara Menjalankan

```bash
cd Tugas_Quiz
python main.py
```
