import tkinter as tk
from tkinter import ttk
import threading
import socket

# -------------------------
# Gradient Background
# -------------------------
def draw_gradient(canvas, w, h, c1, c2):
    r1, g1, b1 = canvas.winfo_rgb(c1)
    r2, g2, b2 = canvas.winfo_rgb(c2)

    r_ratio = (r2 - r1) / h
    g_ratio = (g2 - g1) / h
    b_ratio = (b2 - b1) / h

    for i in range(h):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, i, w, i, fill=color)

# -------------------------
# Scanner GUI
# -------------------------
class SmartScanner(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("🌿 Smart Network Port Scanner")
        self.geometry("900x520")
        self.resizable(False, False)

        # Canvas background
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.update()
        draw_gradient(self.canvas, 900, 520,
                      "#0f9b0f",   # dark green
                      "#00c9a7")   # teal green

        self.build_ui()

    # -------------------------
    # UI Layout
    # -------------------------
    def build_ui(self):

        top_frame = tk.Frame(self, bg="#14532d")
        top_frame.place(x=0, y=0, relwidth=1, height=90)

        tk.Label(top_frame, text="Target:",
                 bg="#14532d", fg="white",
                 font=("Segoe UI", 10, "bold")).place(x=20, y=15)

        self.target_entry = ttk.Entry(top_frame, width=25)
        self.target_entry.place(x=80, y=15)
        self.target_entry.insert(0, "127.0.0.1")

        tk.Label(top_frame, text="Start Port:",
                 bg="#14532d", fg="white",
                 font=("Segoe UI", 10, "bold")).place(x=300, y=15)

        self.start_entry = ttk.Entry(top_frame, width=8)
        self.start_entry.place(x=390, y=15)
        self.start_entry.insert(0, "1")

        tk.Label(top_frame, text="End Port:",
                 bg="#14532d", fg="white",
                 font=("Segoe UI", 10, "bold")).place(x=470, y=15)

        self.end_entry = ttk.Entry(top_frame, width=8)
        self.end_entry.place(x=550, y=15)
        self.end_entry.insert(0, "1024")

        # Buttons
        tk.Button(top_frame, text="Start Scan",
                  bg="#22c55e", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.start_scan).place(x=650, y=10, width=100)

        tk.Button(top_frame, text="Stop",
                  bg="#ef4444", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.stop_scan).place(x=760, y=10, width=80)

        tk.Button(top_frame, text="Clear Output",
                  bg="#334155", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.clear_output).place(x=650, y=50, width=190)

        # Progress Bar
        self.progress = ttk.Progressbar(self)
        self.progress.place(x=40, y=110, width=820)

        # Output box
        self.output = tk.Text(
            self,
            bg="#ecfdf5",
            fg="#064e3b",
            font=("Consolas", 10)
        )
        self.output.place(x=40, y=150, width=820, height=330)

    # -------------------------
    # Scan Logic (Simple Demo)
    # -------------------------
    def scan_ports(self, target, start, end):

        self.output.insert("end", f"Scanning {target}\n\n")

        for port in range(start, end + 1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)

                result = s.connect_ex((target, port))
                if result == 0:
                    self.output.insert("end",
                        f"[OPEN] Port {port}\n")
                    self.output.see("end")

                s.close()
            except:
                pass

        self.output.insert("end", "\nScan Completed ✅\n")

    # -------------------------
    # Button Actions
    # -------------------------
    def start_scan(self):
        target = self.target_entry.get()
        start = int(self.start_entry.get())
        end = int(self.end_entry.get())

        threading.Thread(
            target=self.scan_ports,
            args=(target, start, end),
            daemon=True
        ).start()

    def stop_scan(self):
        self.output.insert("end", "\nStop requested (demo).\n")

    def clear_output(self):
        self.output.delete("1.0", "end")


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app = SmartScanner()
    app.mainloop()