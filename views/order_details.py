import customtkinter as ctk

# Import your color palette from dashboard for consistency
from views.dashboard import ACCENT, TEXT_DARK, TEXT_LIGHT, BTN_BG, BTN_HOVER, HEADER_BG, TABLE_BG

class OrderDetailsModal:
    def __init__(self, parent, values):
        self.modal = ctk.CTkToplevel(parent)
        self.modal.title("Détails de la commande")
        self.modal.geometry("470x570")
        self.modal.focus_set()
        self.modal.attributes('-topmost', True)
        self.modal.after_idle(lambda: self.modal.grab_set())
        self.modal.configure(fg_color=HEADER_BG, corner_radius=14)

        # Shadow effect (simulate by border)
        self.modal._set_appearance_mode("dark")
        border = ctk.CTkFrame(self.modal, fg_color="#222", corner_radius=14)
        border.pack(expand=True, fill="both", padx=8, pady=8)

        # Custom title bar
        titlebar = ctk.CTkFrame(border, fg_color=HEADER_BG, corner_radius=14)
        titlebar.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(titlebar, text=f"Commande #{values[0]}", font=("Arial", 19, "bold"), text_color=ACCENT, fg_color="transparent").pack(side="left", padx=18, pady=10)
        ctk.CTkButton(titlebar, text="✖", width=36, fg_color=BTN_BG, hover_color=BTN_HOVER, command=self.modal.destroy, font=("Arial", 16)).pack(side="right", padx=10, pady=10)

        # Info section
        info = ctk.CTkFrame(border, fg_color=HEADER_BG, corner_radius=10)
        info.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(info, text=f"Client : {values[2]}", font=("Arial", 15), text_color=TEXT_LIGHT, fg_color="transparent").pack(anchor="w", pady=2)
        ctk.CTkLabel(info, text=f"Téléphone : {values[3]}", font=("Arial", 13), text_color=TEXT_LIGHT, fg_color="transparent").pack(anchor="w", pady=2)
        ctk.CTkLabel(info, text=f"Date : {values[1]}", font=("Arial", 13), text_color=ACCENT, fg_color="transparent").pack(anchor="w", pady=2)
        ctk.CTkLabel(info, text=f"Statut : {values[6]}", font=("Arial", 13), text_color=ACCENT, fg_color="transparent").pack(anchor="w", pady=2)
        ctk.CTkLabel(info, text=f"Total : {values[5]}", font=("Arial", 13, "bold"), text_color=ACCENT, fg_color="transparent").pack(anchor="w", pady=(2, 8))

        # Articles section with scrollbar
        articles_lbl = ctk.CTkLabel(border, text="Articles:", font=("Arial", 13, "bold"), text_color=ACCENT, fg_color="transparent")
        articles_lbl.pack(anchor="w", padx=22, pady=(0, 4))
        articles_frame = ctk.CTkFrame(border, fg_color=TABLE_BG, corner_radius=12)
        articles_frame.pack(padx=18, pady=2, fill="both", expand=False)
        articles_box = ctk.CTkTextbox(articles_frame, width=390, height=250, fg_color=TABLE_BG, text_color=TEXT_DARK, font=("Arial", 12), border_width=0, wrap="word")
        articles_box.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
        articles_box.configure(state="normal")
        articles = values[4].split(', ')
        for i in range(0, len(articles), 3):
            line = "   ".join(articles[i:i+3])
            articles_box.insert("end", f" • {line}\n")
        articles_box.configure(state="disabled")

        # Action buttons
        btn_frame = ctk.CTkFrame(border, fg_color="transparent")
        btn_frame.pack(pady=22)
        ctk.CTkButton(btn_frame, text="✏️ Modifier", fg_color=BTN_BG, hover_color=BTN_HOVER, command=lambda: print("Edit"), width=120, height=38, font=("Arial", 13, "bold")).pack(side="left", padx=12)
        ctk.CTkButton(btn_frame, text="🖨️ Imprimer", fg_color=BTN_BG, hover_color=BTN_HOVER, command=lambda: print("Print"), width=120, height=38, font=("Arial", 13, "bold")).pack(side="left", padx=12)
        ctk.CTkButton(btn_frame, text="Fermer", fg_color=HEADER_BG, text_color=TEXT_LIGHT, hover_color="#6f4e37", command=self.modal.destroy, width=120, height=38, font=("Arial", 13, "bold")).pack(side="left", padx=12)

        # Close on Escape
        self.modal.bind("<Escape>", lambda e: self.modal.destroy())
