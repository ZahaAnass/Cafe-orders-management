import customtkinter as ctk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from database.crud import get_orders_stats  

HEADER_BG = "#432818"
BTN_BG = "#a47149"
BTN_HOVER = "#d9ae7e"
ACCENT = "#81c784"
TABLE_BG = "#fff8e1"
TEXT_LIGHT = "#fff8e1"

class ReportsView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Statistiques")
        self.geometry("700x500")
        self.configure(fg_color=HEADER_BG, corner_radius=14)
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Title bar
        titlebar = ctk.CTkFrame(self, fg_color=HEADER_BG, corner_radius=14)
        titlebar.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(titlebar, text=" Statistiques", font=("Arial", 20, "bold"), text_color=ACCENT).pack(side="left", padx=18, pady=14)
        ctk.CTkButton(titlebar, text="❌", width=36, fg_color=BTN_BG, hover_color=BTN_HOVER, command=self.destroy, font=("Arial", 16)).pack(side="right", padx=10, pady=10)

        # Stats summary section
        summary = ctk.CTkFrame(self, fg_color=HEADER_BG)
        summary.pack(fill="x", padx=24, pady=(0, 12))
        # Example: Show total orders and total revenue
        stats = self.get_stats()
        ctk.CTkLabel(summary, text=f"Total commandes : {stats['total_orders']}", font=("Arial", 14, "bold"), text_color=ACCENT).pack(side="left", padx=10)
        ctk.CTkLabel(summary, text=f"Revenu total : {stats['total_revenue']} DH", font=("Arial", 14, "bold"), text_color=ACCENT).pack(side="left", padx=20)

        # Graph area
        graph_frame = ctk.CTkFrame(self, fg_color=TABLE_BG, corner_radius=12)
        graph_frame.pack(expand=True, fill="both", padx=24, pady=12)
        self.plot_orders_per_day(graph_frame)

    def get_stats(self):
        # You should implement get_orders_stats in your database.crud
        # Example return: {'total_orders': 20, 'total_revenue': 1234.56}
        try:
            return get_orders_stats()
        except Exception:
            return {'total_orders': 0, 'total_revenue': 0}

    def plot_orders_per_day(self, frame):
        # Example data: Replace with your own DB query
        import datetime
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        orders = [5, 7, 3, 8, 6, 2, 4]
        # If you have real data, replace above two lines
        fig, ax = plt.subplots(figsize=(6,3.2), dpi=100)
        fig.patch.set_facecolor(TABLE_BG)
        ax.bar(days, orders, color=ACCENT)
        ax.set_title("Commandes par jour", fontsize=14, color=HEADER_BG)
        ax.set_facecolor(TABLE_BG)
        ax.tick_params(axis='x', colors=HEADER_BG)
        ax.tick_params(axis='y', colors=HEADER_BG)
        ax.spines['bottom'].set_color(HEADER_BG)
        ax.spines['left'].set_color(HEADER_BG)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontsize(12)
            label.set_color(HEADER_BG)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")
        plt.close(fig)
