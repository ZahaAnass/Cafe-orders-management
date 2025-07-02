class OrderTable(ctk.CTkTreeview):
    def __init__(self, master, **kw):
        super().__init__(master, columns=("date", "customer", "total", "status"), show="headings", **kw)
        self.column("date", anchor="center", width=100)
        self.column("customer", anchor="center", width=150)
        self.column("total", anchor="center", width=100)
        self.column("status", anchor="center", width=100)
        self.heading("date", text="Date")
        self.heading("customer", text="Customer")
        self.heading("total", text="Total")
        self.heading("status", text="Status")
