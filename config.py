import tkinter as tk
from tkinter import ttk

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text, x, y):
        if self.tipwindow or not text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove border
        tw.wm_geometry(f"+{x+20}+{y+10}")
        label = tk.Label(tw, text=text, background="lightyellow", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack()

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Treeview Tooltip Example")
        self.geometry("400x300")

        self.tree = ttk.Treeview(self, columns=("Order ID", "Name", "Amount"), show="headings")
        self.tree.heading("Order ID", text="Order ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Amount", text="Amount")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tooltip = ToolTip(self.tree)
        self.tree.bind("<Motion>", self.on_hover)
        self.tree.bind("<Leave>", lambda e: self.tooltip.hidetip())

        ZEBRA = "#f0f0f0"
        TABLE_BG = "#ffffff"

        orders = [
            (101, "Alice", "$250"),
            (102, "Bob", "$150"),
            (103, "Carol", "$300"),
        ]

        for i, order in enumerate(orders):
            tag = "zebra" if i % 2 else "normal"
            self.tree.insert("", "end", values=order, tags=(tag,))

        self.tree.tag_configure("zebra", background=ZEBRA)
        self.tree.tag_configure("normal", background=TABLE_BG)

    def on_hover(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.tree.identify_row(event.y)
            column = self.tree.identify_column(event.x)
            if row_id and column:
                cell_value = self.tree.set(row_id, column)
                self.tooltip.showtip(cell_value, self.winfo_pointerx(), self.winfo_pointery())
            else:
                self.tooltip.hidetip()
        else:
            self.tooltip.hidetip()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
