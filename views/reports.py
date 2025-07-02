import customtkinter as ctk
from tkinter import ttk
from models.report import Report
from utils.export import export_to_csv, export_to_pdf
from tkcalendar import DateEntry

class ReportsView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.report = Report()
        self.create_widgets()

    def create_widgets(self):
        # Filters
        filters_frame = ctk.CTkFrame(self, corner_radius=10)
        filters_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(filters_frame, text="Date range:").pack(side="left")
        self.date_range_picker = DateEntry(filters_frame, width=12)
        self.date_range_picker.pack(side="left")

        ttk.Label(filters_frame, text="Product/Category:").pack(side="left")
        self.product_category_filter = ttk.Combobox(filters_frame, values=[""])
        self.product_category_filter.pack(side="left")

        # Report Area
        report_area_frame = ctk.CTkFrame(self, corner_radius=10)
        report_area_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.report_table = ttk.Treeview(report_area_frame)
        self.report_table.pack(fill="both", expand=True)

        # Export Buttons
        export_buttons_frame = ctk.CTkFrame(self, corner_radius=10)
        export_buttons_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(export_buttons_frame, text="Export CSV", command=lambda: export_to_csv(self.report.get_data())).pack(side="left")
        ctk.CTkButton(export_buttons_frame, text="Export PDF", command=lambda: export_to_pdf(self.report.get_data())).pack(side="left")

        # Events
        self.date_range_picker.bind("<<DateEntrySelected>>", self.update_report)
        self.product_category_filter.bind("<<ComboboxSelected>>", self.update_report)

        self.update_report()

    def update_report(self, event=None):
        self.report_table.delete(*self.report_table.get_children())
        data = self.report.get_data(start_date=self.date_range_picker.get_date(), product_category=self.product_category_filter.get())
        for row in data:
            self.report_table.insert("", "end", values=row)
