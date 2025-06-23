import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# --- Palette raffinée ---
PRIMARY_BG = "#f7f3ee"        # Fond général (beige très clair)
HEADER_BG = "#432818"         # Header (marron foncé)
NAV_BG = "#6f4e37"            # Barre nav (marron café)
BTN_BG = "#a47149"            # Boutons (caramel doux)
BTN_HOVER = "#d9ae7e"         # Hover bouton (sable)
TABLE_BG = "#fff8e1"          # Fond tableau (beige pâle)
ZEBRA = "#f4e1c1"             # Lignes alternées
ACCENT = "#81c784"            # Vert doux accent
TEXT_DARK = "#432818"
TEXT_LIGHT = "#fff8e1"

ICON_PATH = os.path.join(os.path.dirname(__file__), "icons")

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=PRIMARY_BG)
        self.create_widgets()

    def create_widgets(self):
        # --- Header immersif ---
        header = ctk.CTkFrame(self, fg_color=HEADER_BG, height=80)
        header.pack(side="top", fill="x")
        ctk.CTkLabel(header, text="☕ Café Manager", font=ctk.CTkFont(size=32, weight="bold"),
                     text_color=ACCENT, fg_color="transparent").pack(side="left", padx=32, pady=10)
        ctk.CTkLabel(header, text="Gérez vos commandes avec élégance",
                     font=ctk.CTkFont(size=17, slant="italic"), text_color=TEXT_LIGHT, fg_color="transparent")\
            .pack(side="left", padx=20, pady=10)

        # --- Zone de stats rapides ---
        stats = ctk.CTkFrame(self, fg_color=PRIMARY_BG)
        stats.pack(fill="x", padx=36, pady=(10, 0))
        stat_style = {"fg_color": "#fff8e1", "corner_radius": 18}
        ctk.CTkLabel(stats, text="Chiffre d'affaires du jour : 21,40 €", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=HEADER_BG, **stat_style).pack(side="left", padx=14, ipadx=12, ipady=8)
        ctk.CTkLabel(stats, text="Commandes du jour : 5", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=HEADER_BG, **stat_style).pack(side="left", padx=14, ipadx=12, ipady=8)
        ctk.CTkLabel(stats, text="Top Article : Café", font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=HEADER_BG, **stat_style).pack(side="left", padx=14, ipadx=12, ipady=8)

        # --- Barre de navigation ---
        nav = ctk.CTkFrame(self, fg_color=NAV_BG, height=54)
        nav.pack(side="top", fill="x", pady=(10, 0))

        btn_style = {"fg_color": BTN_BG, "hover_color": BTN_HOVER, "text_color": TEXT_LIGHT,
                     "corner_radius": 18, "font": ctk.CTkFont(size=15, weight="bold")}

        # Icônes unicode pour chaque bouton (pour l'effet visuel)
        ctk.CTkButton(nav, text="🆕 Nouvelle Commande", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="🔍 Filtrer", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="📊 Statistiques", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="⬇️ Exporter", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="⏻ Quitter", **btn_style, command=self.quit_app).pack(side="right", padx=24, pady=8)

        # --- Tableau des commandes (Treeview stylisé, zebra) ---
        table_frame = ctk.CTkFrame(self, fg_color=TABLE_BG, corner_radius=18)
        table_frame.pack(fill="both", expand=True, padx=36, pady=(18, 12))

        columns = ("date", "client", "table_tel", "articles", "total", "statut")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=11)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=TABLE_BG, foreground=TEXT_DARK,
                        rowheight=38, fieldbackground=TABLE_BG, font=("Segoe UI", 14))
        style.configure("Treeview.Heading",
                        background=BTN_BG, foreground=TEXT_LIGHT,
                        font=("Segoe UI", 15, "bold"), borderwidth=1)
        style.map("Treeview",
                  background=[('selected', ACCENT)],
                  foreground=[('selected', TEXT_DARK)])
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        # En-têtes
        self.tree.heading("date", text="Date")
        self.tree.heading("client", text="Client")
        self.tree.heading("table_tel", text="Table / Téléphone")
        self.tree.heading("articles", text="Articles")
        self.tree.heading("total", text="Total (€)")
        self.tree.heading("statut", text="Statut")

        # Largeurs
        self.tree.column("date", width=120)
        self.tree.column("client", width=150)
        self.tree.column("table_tel", width=140)
        self.tree.column("articles", width=250)
        self.tree.column("total", width=100, anchor="e")
        self.tree.column("statut", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left", padx=6, pady=8)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Données factices avec alternance de couleurs
        fake_orders = [
            ("2025-06-21 09:10", "Alice", "Table 2", "Café, Croissant", "3.70", "en cours"),
            ("2025-06-21 09:15", "Bob", "Tél: 06010203", "Thé, Jus d'orange", "5.00", "livrée"),
            ("2025-06-21 09:30", "Chloé", "Table 1", "Café x2", "3.00", "en cours"),
            ("2025-06-21 09:40", "David", "Tél: 06030405", "Jus d'orange", "3.00", "annulée"),
            ("2025-06-21 10:00", "Emma", "Table 4", "Café, Croissant, Thé", "5.70", "livrée"),
        ]
        for i, order in enumerate(fake_orders):
            tag = "zebra" if i%2 else "normal"
            self.tree.insert("", "end", values=order, tags=(tag,))
        self.tree.tag_configure("zebra", background=ZEBRA)
        self.tree.tag_configure("normal", background=TABLE_BG)

        # --- Footer élégant ---
        footer = ctk.CTkFrame(self, fg_color=HEADER_BG, height=42)
        footer.pack(side="bottom", fill="x")
        ctk.CTkLabel(footer, text="Total commandes affichées : 5",
                     text_color=ACCENT, font=ctk.CTkFont(size=16, weight="bold"), fg_color="transparent")\
            .pack(side="left", padx=22)
        ctk.CTkLabel(footer, text="Café Manager © 2025", text_color=TEXT_LIGHT,
                     font=ctk.CTkFont(size=14), fg_color="transparent").pack(side="right", padx=22)

    def quit_app(self):
        self.winfo_toplevel().destroy()
