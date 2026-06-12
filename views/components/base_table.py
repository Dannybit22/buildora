import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class BaseTable(ctk.CTkFrame):
    def __init__(self, master, columns, headings):
        super().__init__(master, fg_color="transparent")

        self.columns = columns
        self.headings = headings

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings",
            height=14
        )

        for column in self.columns:
            self.tree.heading(column, text=self.headings.get(column, column))
            self.tree.column(column, width=140, anchor="center")

        self.scroll_y = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.scroll_x = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure_style()

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1E1E1E",
            foreground="white",
            fieldbackground="#1E1E1E",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#F4C430",
            foreground="black",
            font=("Arial", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#333333")]
        )

    def load_data(self, data):
        self.clear()

        for row in data:
            values = [row.get(column, "") for column in self.columns]
            self.tree.insert("", "end", values=values)

    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_selected_values(self):
        selected = self.tree.selection()

        if not selected:
            return None

        item = self.tree.item(selected[0])
        return item["values"]