
import tkinter as tk
from tkinter import ttk


class ResponsiveApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Responsive Design dengan ttk")
        self.root.geometry("800x600")
        self.root.minsize(400, 400)

        # Variabel untuk tracking ukuran window
        self.current_width = 800
        self.current_height = 600

        self._setup_styles()
        self._buat_interface()
        self._bind_events()

    def _setup_styles(self):
        self.style = ttk.Style()

        # Style untuk desktop (default)
        self.style.configure(
            'Desktop.TLabel',
            font=('Arial', 12),
            padding=(10, 5)
        )

        # Style untuk tablet
        self.style.configure(
            'Tablet.TLabel',
            font=('Arial', 10),
            padding=(8, 4)
        )

        # Style untuk mobile
        self.style.configure(
            'Mobile.TLabel',
            font=('Arial', 9),
            padding=(5, 3)
        )

        # Button styles
        self.style.configure(
            'Desktop.TButton',
            padding=(15, 8),
            font=('Arial', 11)
        )

        self.style.configure(
            'Tablet.TButton',
            padding=(12, 6),
            font=('Arial', 10)
        )

        self.style.configure(
            'Mobile.TButton',
            padding=(8, 4),
            font=('Arial', 9)
        )

    def _buat_interface(self):
        # Main container dengan scrollable frame
        self.canvas = tk.Canvas(self.root)

        self.scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        # Menyesuaikan lebar frame dengan canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(
                self.window_id,
                width=e.width
            )
        )

        # Header section
        self.header_frame = ttk.Frame(
            self.scrollable_frame
        )
        self.header_frame.pack(
            fill='x',
            padx=20,
            pady=20
        )

        self.title_label = ttk.Label(
            self.header_frame,
            text="Responsive Design Demo",
            style='Desktop.TLabel'
        )
        self.title_label.pack()

        self.size_label = ttk.Label(
            self.header_frame,
            text=f"Window Size: {self.current_width}x{self.current_height}",
            style='Desktop.TLabel'
        )
        self.size_label.pack(pady=(5, 0))

        # Content grid yang akan berubah layout
        self.content_frame = ttk.Frame(
            self.scrollable_frame
        )
        self.content_frame.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Cards
        self.cards = []

        for i in range(6):
            card = ttk.LabelFrame(
                self.content_frame,
                text=f"Card {i+1}",
                padding="15"
            )

            ttk.Label(
                card,
                text=f"Content untuk card {i+1}",
                style='Desktop.TLabel'
            ).pack()

            ttk.Button(
                card,
                text=f"Action {i+1}",
                style='Desktop.TButton'
            ).pack(pady=(10, 0))

            self.cards.append(card)

        # Control panel
        self.control_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text="Controls",
            padding="15"
        )
        self.control_frame.pack(
            fill='x',
            padx=20,
            pady=(0, 20)
        )

        ttk.Button(
            self.control_frame,
            text="Simulate Mobile (400x600)",
            command=lambda: self.resize_window(400, 600),
            style='Desktop.TButton'
        ).pack(side='left', padx=(0, 10))

        ttk.Button(
            self.control_frame,
            text="Simulate Tablet (600x800)",
            command=lambda: self.resize_window(600, 800),
            style='Desktop.TButton'
        ).pack(side='left', padx=(0, 10))

        ttk.Button(
            self.control_frame,
            text="Simulate Desktop (800x600)",
            command=lambda: self.resize_window(800, 600),
            style='Desktop.TButton'
        ).pack(side='left')

        # Pack canvas dan scrollbar
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        # Initial layout
        self.root.after(100, self._update_layout)

    def _bind_events(self):
        self.root.bind(
            '<Configure>',
            self._on_window_resize
        )

    def _on_window_resize(self, event):
        if event.widget == self.root:
            self.current_width = self.root.winfo_width()
            self.current_height = self.root.winfo_height()

            self.size_label.config(
                text=f"Window Size: {self.current_width}x{self.current_height}"
            )

            self._update_layout()

    def _update_layout(self):
        # Clear current layout
        for card in self.cards:
            card.grid_forget()

        # Determine layout based on window width
        if self.current_width < 500:
            self._apply_mobile_layout()

        elif self.current_width < 700:
            self._apply_tablet_layout()

        else:
            self._apply_desktop_layout()

    def _apply_mobile_layout(self):
        # Single column layout
        for i, card in enumerate(self.cards):
            card.grid(
                row=i,
                column=0,
                sticky='nsew',
                padx=5,
                pady=5
            )

        self.content_frame.columnconfigure(0, weight=1)

        self._update_styles('Mobile')

    def _apply_tablet_layout(self):
        # Two column layout
        for i, card in enumerate(self.cards):
            row = i // 2
            col = i % 2

            card.grid(
                row=row,
                column=col,
                sticky='nsew',
                padx=5,
                pady=5
            )

        for col in range(2):
            self.content_frame.columnconfigure(
                col,
                weight=1
            )

        self._update_styles('Tablet')

    def _apply_desktop_layout(self):
        # Three column layout
        for i, card in enumerate(self.cards):
            row = i // 3
            col = i % 3

            card.grid(
                row=row,
                column=col,
                sticky='nsew',
                padx=5,
                pady=5
            )

        for col in range(3):
            self.content_frame.columnconfigure(
                col,
                weight=1
            )

        self._update_styles('Desktop')

    def _update_styles(self, size):
        style_suffix = f'{size}.TLabel'
        button_style = f'{size}.TButton'

        self.title_label.config(style=style_suffix)
        self.size_label.config(style=style_suffix)

        # Update semua label dan button dalam cards
        for card in self.cards:
            for child in card.winfo_children():

                if isinstance(child, ttk.Label):
                    child.config(style=style_suffix)

                elif isinstance(child, ttk.Button):
                    child.config(style=button_style)

    def resize_window(self, width, height):
        self.root.geometry(f"{width}x{height}")

    def run(self):
        self.root.mainloop()


# Jalankan aplikasi
if __name__ == "__main__":
    app = ResponsiveApp()
    app.run()
