import customtkinter as ctk
from tkinter import ttk
from database.crud import createOrder, updateOrder, get_all_products
from utils.validators import validate_customer, validate_order_item, validate_order_status

PRIMARY_BG = "#f7f3ee"
HEADER_BG = "#432818"
NAV_BG = "#6f4e37"
BTN_BG = "#a47149"
BTN_HOVER = "#d9ae7e"
TABLE_BG = "#fff8e1"
ZEBRA = "#f4e1c1"
ACCENT = "#81c784"
TEXT_DARK = "#432818"
TEXT_LIGHT = "#fff8e1"

class OrderForm(ctk.CTkToplevel):
    def __init__(self, parent, order=None):
        super().__init__(parent)
        self.order = order
        self.title("Order Form")
        self.geometry("600x600")
        self.configure(fg_color=HEADER_BG, corner_radius=14)
        # Extract product names for combobox
        self.products = [p[1] for p in get_all_products()]
        self.create_widgets()

    def create_widgets(self):
        border = ctk.CTkFrame(self, fg_color="#222", corner_radius=14)
        border.pack(expand=True, fill="both", padx=12, pady=12)

        # Title bar
        titlebar = ctk.CTkFrame(border, fg_color=HEADER_BG, corner_radius=14)
        titlebar.pack(fill="x", pady=(0, 6))
        ctk.CTkLabel(titlebar, text="📝 Nouvelle commande" if not self.order else "📝 Modifier la commande", font=("Arial", 18, "bold"), text_color=ACCENT).pack(side="left", padx=18, pady=10)
        ctk.CTkButton(titlebar, text="✖", width=36, fg_color=BTN_BG, hover_color=BTN_HOVER, command=self.destroy, font=("Arial", 16)).pack(side="right", padx=10, pady=10)

        # Customer info section
        info = ctk.CTkFrame(border, fg_color=HEADER_BG, corner_radius=10)
        info.pack(fill="x", padx=20, pady=(0, 14))
        ctk.CTkLabel(info, text="Client :", font=("Arial", 14, "bold"), text_color=ACCENT).pack(anchor="w", pady=(4,0))
        fields = ctk.CTkFrame(info, fg_color=HEADER_BG)
        fields.pack(fill="x", pady=(0, 6))
        self.name_entry = ctk.CTkEntry(fields, placeholder_text="Nom")
        self.name_entry.pack(side="left", padx=5, pady=4, expand=True, fill="x")
        self.phone_entry = ctk.CTkEntry(fields, placeholder_text="Téléphone")
        self.phone_entry.pack(side="left", padx=5, pady=4, expand=True, fill="x")
        self.email_entry = ctk.CTkEntry(fields, placeholder_text="Email")
        self.email_entry.pack(side="left", padx=5, pady=4, expand=True, fill="x")

        # Order items section with scroll
        ctk.CTkLabel(border, text="Articles :", font=("Arial", 13, "bold"), text_color=ACCENT).pack(anchor="w", padx=22, pady=(0, 4))
        items_outer = ctk.CTkFrame(border, fg_color=TABLE_BG, corner_radius=12)
        items_outer.pack(padx=18, pady=(2, 0), fill="both", expand=False)
        self.items_canvas = ctk.CTkCanvas(items_outer, bg=TABLE_BG, highlightthickness=0, height=180)
        self.items_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ctk.CTkScrollbar(items_outer, orientation="vertical", command=self.items_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.items_canvas.configure(yscrollcommand=scrollbar.set)
        self.order_items_frame = ctk.CTkFrame(self.items_canvas, fg_color=TABLE_BG)
        self.items_canvas.create_window((0,0), window=self.order_items_frame, anchor="nw")
        self.order_items_frame.bind("<Configure>", lambda e: self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all")))

        # Add Article button
        self.add_product_row_btn = ctk.CTkButton(border, text="➕ Ajouter un article", fg_color=BTN_BG, hover_color=BTN_HOVER, command=self.add_product_row)
        self.add_product_row_btn.pack(pady=(12, 16))

        # Status section
        status_frame = ctk.CTkFrame(border, fg_color=HEADER_BG)
        status_frame.pack(fill="x", padx=20, pady=(6, 14))
        ctk.CTkLabel(status_frame, text="Statut :", font=("Arial", 13, "bold"), text_color=ACCENT).pack(side="left", padx=(0, 10))
        self.status_entry = ttk.Combobox(status_frame, values=["Pending", "Preparing", "Served", "Paid"])
        self.status_entry.pack(side="left", fill="x", expand=True, padx=5, pady=4)

        # Error label
        self.error_label = ctk.CTkLabel(border, text="", text_color="red")
        self.error_label.pack(anchor="w", padx=22, pady=(0, 14))

        # Action buttons
        btn_frame = ctk.CTkFrame(border, fg_color="transparent")
        btn_frame.pack(pady=18)
        ctk.CTkButton(btn_frame, text="💾 Enregistrer", fg_color=BTN_BG, hover_color=BTN_HOVER, command=self.save, width=120, height=38, font=("Arial", 13, "bold")).pack(side="left", padx=12)
        ctk.CTkButton(btn_frame, text="Annuler", fg_color=HEADER_BG, text_color=TEXT_LIGHT, hover_color="#6f4e37", command=self.destroy, width=120, height=38, font=("Arial", 13, "bold")).pack(side="left", padx=12)

        # Pre-fill for edit
        if self.order:
            self.name_entry.insert(0, self.order["customer"]["name"])
            self.phone_entry.insert(0, self.order["customer"]["phone"])
            self.email_entry.insert(0, self.order["customer"]["email"])
            for item in self.order["items"]:
                self.add_product_row(product=item["product"], quantity=item["quantity"], price=item["price"])
            self.status_entry.set(self.order["status"])
        else:
            self.add_product_row()

    def add_product_row(self, product=None, quantity=None, price=None):
        frame = ctk.CTkFrame(self.order_items_frame, fg_color=TABLE_BG)
        frame.pack(fill="x", pady=7)  # More vertical space between rows
        product_entry = ttk.Combobox(frame, values=self.products, width=22)
        product_entry.pack(side="left", padx=8)
        if product:
            product_entry.set(product)
        quantity_entry = ctk.CTkEntry(frame, width=120, placeholder_text="Quantity")
        quantity_entry.pack(side="left", padx=8)
        if quantity:
            quantity_entry.insert(0, quantity)
        price_entry = ctk.CTkEntry(frame, width=120, placeholder_text="Price")
        price_entry.pack(side="left", padx=8)
        if price:
            price_entry.insert(0, price)
        remove_button = ctk.CTkButton(frame, text="❌", width=32, fg_color=BTN_BG, hover_color=BTN_HOVER, command=lambda: frame.destroy())
        remove_button.pack(side="left", padx=8)

    def save(self):
        if not validate_customer(self.name_entry.get(), self.phone_entry.get(), self.email_entry.get()):
            self.error_label.configure(text="Invalid customer information")
            return
        order_items = []
        for child in self.order_items_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                widgets = child.winfo_children()
                product = widgets[0].get()
                quantity = widgets[1].get()
                price = widgets[2].get()
                if not validate_order_item(product, quantity, price):
                    self.error_label.configure(text="Invalid order item information")
                    return
                order_items.append({
                    "product": product,
                    "quantity": int(quantity),
                    "price": float(price)
                })
        status = self.status_entry.get()
        if not validate_order_status(status):
            self.error_label.configure(text="Invalid order status")
            return
        if self.order:
            updateOrder(self.order["id"], {
                "customer": {
                    "name": self.name_entry.get(),
                    "phone": self.phone_entry.get(),
                    "email": self.email_entry.get()
                },
                "items": order_items,
                "status": status
            })
        else:
            createOrder({
                "customer": {
                    "name": self.name_entry.get(),
                    "phone": self.phone_entry.get(),
                    "email": self.email_entry.get()
                },
                "items": order_items,
                "status": status
            })
        self.destroy()