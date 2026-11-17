import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random


class InteractiveDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive Dashboard - Real-time Updates")
        self.root.geometry("1000x700")
        self.root.minsize(750, 550)
        self.root.configure(bg="#0f1419")

        # Status dan data simulasi
        self.is_running = False
        self.monitor_job = None
        self.time_job = None

        self.cpu_data = []
        self.memory_data = []
        self.network_data = []
        self.max_data_points = 50

        self.current_cpu = 0
        self.current_memory = 0
        self.current_network = 0.0
        self.total_requests = 0
        self.active_users = 0

        self._setup_styles()
        self._buat_interface()
        self._update_time()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Dashboard.TFrame", background="#1e2328"
        )
        self.style.configure(
            "Card.TFrame",
            background="#252a31",
            relief="raised",
            borderwidth=1
        )
        self.style.configure(
            "Dashboard.TLabel",
            background="#1e2328",
            foreground="#ffffff",
            font=("Arial", 10)
        )
        self.style.configure(
            "Title.TLabel",
            background="#1e2328",
            foreground="#00d4ff",
            font=("Arial", 16, "bold")
        )
        self.style.configure(
            "Metric.TLabel",
            background="#252a31",
            foreground="#00ff88",
            font=("Arial", 20, "bold")
        )
        self.style.configure(
            "MetricLabel.TLabel",
            background="#252a31",
            foreground="#ffffff",
            font=("Arial", 9)
        )
        self.style.configure(
            "Control.TButton",
            background="#00b8d9",
            foreground="#0f1419",
            padding=(12, 8),
            font=("Arial", 9, "bold")
        )
        self.style.map(
            "Control.TButton",
            background=[("active", "#00d4ff"), ("pressed", "#008eaa")]
        )
        self.style.configure(
            "TProgressbar",
            troughcolor="#3b424a",
            background="#00d4ff",
            thickness=14
        )

    def _buat_interface(self):
        self.main_frame = ttk.Frame(
            self.root, style="Dashboard.TFrame", padding=15
        )
        self.main_frame.pack(fill="both", expand=True)

        # Header
        header_frame = ttk.Frame(
            self.main_frame, style="Dashboard.TFrame"
        )
        header_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            header_frame, text="📊 System Dashboard",
            style="Title.TLabel"
        ).pack(side="left")

        self.status_label = ttk.Label(
            header_frame, text="● Stopped",
            style="Dashboard.TLabel", foreground="#ff6666"
        )
        self.status_label.pack(side="right")

        self.time_label = ttk.Label(
            header_frame, text="",
            style="Dashboard.TLabel"
        )
        self.time_label.pack(side="right", padx=(0, 20))

        # Metrics cards
        metrics_frame = ttk.Frame(
            self.main_frame, style="Dashboard.TFrame"
        )
        metrics_frame.pack(fill="x", pady=(0, 15))

        self.cpu_metric, self.cpu_progress = self._create_metric_card(
            metrics_frame, "CPU Usage", "0%"
        )
        self.memory_metric, self.memory_progress = self._create_metric_card(
            metrics_frame, "Memory Usage", "0%"
        )
        self.network_metric, self.network_progress = self._create_metric_card(
            metrics_frame, "Network I/O", "0 MB/s"
        )

        # Statistics
        stats_frame = ttk.Frame(
            self.main_frame, style="Dashboard.TFrame"
        )
        stats_frame.pack(fill="x", pady=(0, 15))

        self.requests_metric = self._create_stat_card(
            stats_frame, "Total Requests", "0"
        )
        self.users_metric = self._create_stat_card(
            stats_frame, "Active Users", "0"
        )

        # Monitoring output
        chart_frame = ttk.LabelFrame(
            self.main_frame, text="Real-time Monitoring (Simulated)",
            padding=10
        )
        chart_frame.pack(fill="both", expand=True, pady=(0, 15))

        text_frame = ttk.Frame(chart_frame)
        text_frame.pack(fill="both", expand=True)

        self.chart_text = tk.Text(
            text_frame, height=12, bg="#0f1419", fg="#00ff88",
            insertbackground="white", font=("Consolas", 9),
            state="disabled", wrap="none"
        )
        scrollbar = ttk.Scrollbar(
            text_frame, orient="vertical", command=self.chart_text.yview
        )
        self.chart_text.configure(yscrollcommand=scrollbar.set)

        self.chart_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Controls
        control_frame = ttk.Frame(
            self.main_frame, style="Dashboard.TFrame"
        )
        control_frame.pack(fill="x")

        ttk.Button(
            control_frame, text="▶ Start Monitoring",
            style="Control.TButton", command=self.start_monitoring
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            control_frame, text="⏸ Stop Monitoring",
            style="Control.TButton", command=self.stop_monitoring
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            control_frame, text="🗑 Clear Data",
            style="Control.TButton", command=self.clear_data
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            control_frame, text="📊 Generate Report",
            style="Control.TButton", command=self.generate_report
        ).pack(side="right")

    def _create_metric_card(self, parent, title, initial_value):
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(
            card, text=title, style="MetricLabel.TLabel"
        ).pack()

        metric = ttk.Label(
            card, text=initial_value, style="Metric.TLabel"
        )
        metric.pack(pady=(5, 8))

        progress = ttk.Progressbar(
            card, mode="determinate", maximum=100
        )
        progress.pack(fill="x")

        return metric, progress

    def _create_stat_card(self, parent, title, initial_value):
        card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        card.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(
            card, text=title, style="MetricLabel.TLabel"
        ).pack()

        metric = ttk.Label(
            card, text=initial_value, style="Metric.TLabel"
        )
        metric.pack(pady=(5, 0))

        return metric

    def _update_time(self):
        self.time_label.config(
            text=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.time_job = self.root.after(1000, self._update_time)

    def start_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(
                text="● Running", foreground="#00ff88"
            )
            self._monitoring_loop()

    def stop_monitoring(self):
        self.is_running = False
        if self.monitor_job is not None:
            self.root.after_cancel(self.monitor_job)
            self.monitor_job = None
        self.status_label.config(
            text="● Stopped", foreground="#ff6666"
        )

    def _monitoring_loop(self):
        if not self.is_running:
            return

        # Nilai acak untuk simulasi, bukan pembacaan CPU/RAM komputer asli.
        self.current_cpu = random.randint(10, 90)
        self.current_memory = random.randint(20, 80)
        self.current_network = random.uniform(0.1, 10.0)

        self.total_requests += random.randint(1, 5)
        self.active_users = random.randint(50, 200)

        self.cpu_data.append(self.current_cpu)
        self.memory_data.append(self.current_memory)
        self.network_data.append(self.current_network)

        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.network_data.pop(0)

        self._update_metrics()
        self._update_chart()

        self.monitor_job = self.root.after(1000, self._monitoring_loop)

    def _update_metrics(self):
        self.cpu_metric.config(text=f"{self.current_cpu}%")
        self.cpu_progress["value"] = self.current_cpu

        self.memory_metric.config(text=f"{self.current_memory}%")
        self.memory_progress["value"] = self.current_memory

        self.network_metric.config(
            text=f"{self.current_network:.1f} MB/s"
        )
        self.network_progress["value"] = min(
            self.current_network * 10, 100
        )

        self.requests_metric.config(text=str(self.total_requests))
        self.users_metric.config(text=str(self.active_users))

    def _update_chart(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        cpu_bar = "█" * (self.current_cpu // 5)
        memory_bar = "█" * (self.current_memory // 5)
        network_bar = "█" * min(int(self.current_network), 20)

        chart_line = (
            f"[{timestamp}] CPU: {cpu_bar:<18} {self.current_cpu:>2}% | "
            f"MEM: {memory_bar:<18} {self.current_memory:>2}% | "
            f"NET: {network_bar:<10} {self.current_network:.1f} MB/s\n"
        )

        self.chart_text.config(state="normal")
        self.chart_text.insert("end", chart_line)
        self.chart_text.see("end")
        self.chart_text.config(state="disabled")

    def clear_data(self):
        self.cpu_data.clear()
        self.memory_data.clear()
        self.network_data.clear()
        self.total_requests = 0
        self.active_users = 0
        self.current_cpu = 0
        self.current_memory = 0
        self.current_network = 0.0

        self.cpu_metric.config(text="0%")
        self.memory_metric.config(text="0%")
        self.network_metric.config(text="0 MB/s")
        self.requests_metric.config(text="0")
        self.users_metric.config(text="0")

        self.cpu_progress["value"] = 0
        self.memory_progress["value"] = 0
        self.network_progress["value"] = 0

        self.chart_text.config(state="normal")
        self.chart_text.delete("1.0", "end")
        self.chart_text.config(state="disabled")

    def generate_report(self):
        if not self.cpu_data:
            self.chart_text.config(state="normal")
            self.chart_text.insert(
                "end",
                "Belum ada data. Klik Start Monitoring terlebih dahulu.\n"
            )
            self.chart_text.see("end")
            self.chart_text.config(state="disabled")
            return

        avg_cpu = sum(self.cpu_data) / len(self.cpu_data)
        avg_memory = sum(self.memory_data) / len(self.memory_data)
        avg_network = sum(self.network_data) / len(self.network_data)

        report = (
            "\n" + "=" * 58 + "\n"
            f"SYSTEM PERFORMANCE REPORT - "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            + "=" * 58 + "\n"
            f"Average CPU Usage: {avg_cpu:.1f}%\n"
            f"Average Memory Usage: {avg_memory:.1f}%\n"
            f"Average Network I/O: {avg_network:.1f} MB/s\n"
            f"Total Requests: {self.total_requests}\n"
            f"Current Active Users: {self.active_users}\n"
            f"Data Points Collected: {len(self.cpu_data)}\n"
            + "=" * 58 + "\n\n"
        )

        self.chart_text.config(state="normal")
        self.chart_text.insert("end", report)
        self.chart_text.see("end")
        self.chart_text.config(state="disabled")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = InteractiveDashboard()
    app.run()
