import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from views.order_form import OrderForm
from views.reports import ReportsView
from database.crud import *
from CTkToolTip import CTkToolTip

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

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.visible = False
        self.current_row = None

    def showtip(self, text, x, y, row_id=None):
        # Only update if it's a new row or no tooltip is shown
        if self.current_row != row_id:
            self.hidetip()  # Hide previous tooltip if any
            
        if self.tipwindow or not text:
            return
            
        self.current_row = row_id
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x+20}+{y+10}")
        tw.attributes('-topmost', True)
        
        # Make tooltip stay on hover
        tw.bind("<Enter>", lambda e: None)  # Keep tooltip when hovering over it
        tw.bind("<Leave>", lambda e: self.hidetip())
        
        # Main container with padding
        container = ctk.CTkFrame(tw, fg_color="#2b2b2b", corner_radius=8)
        container.pack(padx=1, pady=1)
        
        # Title with order info
        title = ctk.CTkLabel(
            container,
            text="Détails de la commande",
            font=("Arial", 12, "bold"),
            text_color="#4cc9f0",
            anchor="w"
        )
        title.pack(fill="x", padx=10, pady=(10, 5))
        
        # Separator
        ctk.CTkFrame(container, height=1, fg_color="#444").pack(fill="x", padx=5)
        
        # Content with better formatting
        content = ctk.CTkTextbox(
            container,
            width=300,
            height=500,
            fg_color="#2b2b2b",
            text_color="white",
            border_width=0,
            font=("Arial", 11),
            wrap="word",
            activate_scrollbars=True
        )
        content.pack(padx=10, pady=5, fill="both", expand=True)
        content.insert("1.0", text)
        content.configure(state="disabled")  # Make it read-only
        
        # Add a subtle shadow effect
        for i in range(3):
            ctk.CTkFrame(
                tw,
                width=2,
                height=2,
                fg_color="black",
                corner_radius=1
            ).place(x=i, y=i, relx=1, rely=1, anchor="se")
        
        self.visible = True

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
            self.visible = False
            self.current_row = None

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color=PRIMARY_BG)
        self.create_widgets()

    def on_tree_single_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            if row_id:
                values = self.tree.item(row_id, 'values')
                if values:
                    # Compact tooltip: client, total, status
                    tooltip_lines = [
                        f"Commande #{values[0]}",
                        f"📅 {values[1]}",
                        f"👤 {values[2]}",
                        f"💶 Total: {values[5]}",
                        f"🟢 {values[6]}",
                        f"🗃️Articles: \n{values[4]}"
                    ]
                    tooltip_text = "\n".join(tooltip_lines)
                    self.tooltip.showtip(tooltip_text, event.x_root, event.y_root, row_id)
        else:
            if hasattr(self, 'tooltip') and not getattr(self.tooltip, 'tipwindow', None):
                self.tooltip.hidetip()

    def on_tree_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            if row_id:
                values = self.tree.item(row_id, 'values')
                if values:
                    self.show_order_details_modal(values)

    def show_order_details_modal(self, values):
        # Hide any tooltip before showing the modal
        if hasattr(self, "tooltip"):
            self.tooltip.hidetip()
        from views.order_details import OrderDetailsModal
        OrderDetailsModal(self, values)


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
        ctk.CTkButton(nav, text="🆕 Nouvelle Commande", **btn_style, command=lambda: OrderForm(self)).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="🔍 Filtrer", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="📊 Statistiques", **btn_style, command= lambda : ReportsView(self)).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="⬇️ Exporter", **btn_style).pack(side="left", padx=10, pady=8)
        ctk.CTkButton(nav, text="⏻ Quitter", **btn_style, command=self.quit_app).pack(side="right", padx=24, pady=8)

        # --- Tableau des commandes (Treeview stylisé, zebra) ---
        table_frame = ctk.CTkFrame(self, fg_color=TABLE_BG, corner_radius=18)
        table_frame.pack(fill="both", expand=True, padx=36, pady=(18, 12))

        columns = ("order_id", "date", "client", "table_tel", "articles", "total", "statut")
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
        self.tree.heading("order_id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("client", text="Client")
        self.tree.heading("table_tel", text="Table / Téléphone")
        self.tree.heading("articles", text="Articles")
        self.tree.heading("total", text="Total (€)")
        self.tree.heading("statut", text="Statut")

        # Largeurs
        self.tree.column("order_id", width=60)
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

        orders = getTable()

        for i, order in enumerate(orders):
            tag = "zebra" if i%2 else "normal"
            self.tree.insert("", "end", values=order, tags=(tag,))
        self.tree.tag_configure("zebra", background=ZEBRA)
        self.tree.tag_configure("normal", background=TABLE_BG)
        self.tooltip = ToolTip(self.tree)
        self.tree.bind("<Button-1>", self.on_tree_single_click)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Leave>", lambda e: self.tooltip.hidetip() if not getattr(self.tooltip, 'visible', False) else None)
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
