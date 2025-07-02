import customtkinter as ctk
class StatsCard(ctk.CTkFrame):
    """Small card for displaying a stat."""

    def __init__(self, master, text, value, **kwargs):
        super().__init__(master, fg_color="gray", corner_radius=10, **kwargs)
        self.text = text
        self.value = value

        # Stat label
        stat_label = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=14, weight="bold"))
        stat_label.pack(pady=8)

        # Stat value
        stat_value = ctk.CTkLabel(self, text=str(value), font=ctk.CTkFont(size=24, weight="bold"))
        stat_value.pack(pady=8)
