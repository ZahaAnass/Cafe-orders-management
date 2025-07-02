import customtkinter as ctk
from views.dashboard import Dashboard
from database.database import init_db

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Commandes de Café")
        self.geometry("1100x650")
        self.dashboard = Dashboard(self)
        self.dashboard.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # ou "system" ou "dark"
    app = App()
    # init_db()
    app.mainloop()