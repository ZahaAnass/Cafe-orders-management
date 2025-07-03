import customtkinter as ctk
from views.dashboard import Dashboard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Commandes de Café")
        self.geometry("1200x700")
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # ou "system" ou "dark"
    app = App()
    app.mainloop()