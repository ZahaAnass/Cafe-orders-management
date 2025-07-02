import customtkinter as ctk
from tkinter import ttk
from database.crud import createOrder, updateOrder
from utils.validators import validate_customer, validate_order_item, validate_order_status

class OrderForm(ctk.CTkToplevel):
    def __init__(self, parent, order=None):
        super().__init__(parent)
        self.order = order
        self.title("Order Form")
        self.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        self.customer_info_frame = ctk.CTkFrame(self)
        self.customer_info_frame.pack(fill="x")
        self.name_label = ctk.CTkLabel(self.customer_info_frame, text="Name:")
        self.name_label.pack(side="left")
        self.name_entry = ctk.CTkEntry(self.customer_info_frame)
        self.name_entry.pack(side="left")
        self.phone_label = ctk.CTkLabel(self.customer_info_frame, text="Phone:")
        self.phone_label.pack(side="left")
        self.phone_entry = ctk.CTkEntry(self.customer_info_frame)
        self.phone_entry.pack(side="left")
        self.email_label = ctk.CTkLabel(self.customer_info_frame, text="Email:")
        self.email_label.pack(side="left")
        self.email_entry = ctk.CTkEntry(self.customer_info_frame)
        self.email_entry.pack(side="left")

        self.order_items_frame = ctk.CTkFrame(self)
        self.order_items_frame.pack(fill="x")
        self.product_label = ctk.CTkLabel(self.order_items_frame, text="Product:")
        self.product_label.pack(side="left")
        self.product_entry = ttk.Combobox(self.order_items_frame, values=[""])
        self.product_entry.pack(side="left")
        self.quantity_label = ctk.CTkLabel(self.order_items_frame, text="Quantity:")
        self.quantity_label.pack(side="left")
        self.quantity_entry = ctk.CTkEntry(self.order_items_frame)
        self.quantity_entry.pack(side="left")
        self.price_label = ctk.CTkLabel(self.order_items_frame, text="Price:")
        self.price_label.pack(side="left")
        self.price_entry = ctk.CTkEntry(self.order_items_frame)
        self.price_entry.pack(side="left")
        self.remove_button = ctk.CTkButton(self.order_items_frame, text="Remove")
        self.remove_button.pack(side="left")

        self.add_button = ctk.CTkButton(self.order_items_frame, text="Add", command=self.add_product_row)
        self.add_button.pack(side="left")

        self.order_status_frame = ctk.CTkFrame(self)
        self.order_status_frame.pack(fill="x")
        self.status_label = ctk.CTkLabel(self.order_status_frame, text="Status:")
        self.status_label.pack(side="left")
        self.status_entry = ttk.Combobox(self.order_status_frame, values=["Pending", "Preparing", "Served", "Paid"])
        self.status_entry.pack(side="left")

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save)
        self.save_button.pack()
        self.cancel_button = ctk.CTkButton(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack()

        if self.order:
            self.name_entry.insert(0, self.order["customer"]["name"])
            self.phone_entry.insert(0, self.order["customer"]["phone"])
            self.email_entry.insert(0, self.order["customer"]["email"])
            for item in self.order["items"]:
                self.add_product_row(product=item["product"], quantity=item["quantity"], price=item["price"])
            self.status_entry.set(self.order["status"])

    def add_product_row(self, product=None, quantity=None, price=None):
        frame = ctk.CTkFrame(self.order_items_frame)
        frame.pack(fill="x")
        product_label = ctk.CTkLabel(frame, text="Product:")
        product_label.pack(side="left")
        product_entry = ttk.Combobox(frame, values=[""])
        product_entry.pack(side="left")
        if product:
            product_entry.set(product)
        quantity_label = ctk.CTkLabel(frame, text="Quantity:")
        quantity_label.pack(side="left")
        quantity_entry = ctk.CTkEntry(frame)
        quantity_entry.pack(side="left")
        if quantity:
            quantity_entry.insert(0, quantity)
        price_label = ctk.CTkLabel(frame, text="Price:")
        price_label.pack(side="left")
        price_entry = ctk.CTkEntry(frame)
        price_entry.pack(side="left")
        if price:
            price_entry.insert(0, price)
        remove_button = ctk.CTkButton(frame, text="Remove", command=lambda: frame.destroy())
        remove_button.pack(side="left")

    def save(self):
        if not validate_customer(self.name_entry.get(), self.phone_entry.get(), self.email_entry.get()):
            return
        order_items = []
        for child in self.order_items_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                product = child.winfo_children()[1].get()
                quantity = child.winfo_children()[3].get()
                price = child.winfo_children()[5].get()
                if not validate_order_item(product, quantity, price):
                    return
                order_items.append({
                    "product": product,
                    "quantity": int(quantity),
                    "price": float(price)
                })
        status = self.status_entry.get()
        if not validate_order_status(status):
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