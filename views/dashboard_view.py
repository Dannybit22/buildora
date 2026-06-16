import customtkinter as ctk

from controllers.dashboard_controller import DashboardController
from views.components.base_table import BaseTable
from config.app_config import COLOR_PANEL, COLOR_TEXT, COLOR_MUTED_TEXT, COLOR_PRIMARY
from PIL import Image
import os

class DashboardView(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master, fg_color=COLOR_PANEL)

        self.user = user
        self.controller = DashboardController()

        self.summary = self.controller.get_summary()

        self.create_widgets()

    def create_widgets(self):
        logo_path = os.path.join("assets", "buildora_logob.jpg")

        img = Image.open(logo_path)

        logo_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(200, 57)
        )

        logo_label = ctk.CTkLabel(
            self,
            image=logo_image,
            text=""
        )

        logo_label.image = logo_image
        logo_label.pack(pady=(15, 5))

        subtitle = ctk.CTkLabel(
            self,
            text=f"Hola!, {self.user['nombres']} {self.user['apellidos']} | Rol: {self.user['nombre_rol']}",
            font=("Arial", 14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(pady=(0, 20))

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=25, pady=10)

        self.create_card(cards_frame, "Clientes", self.summary["clientes"], 0, 0)
        self.create_card(cards_frame, "Proyectos", self.summary["proyectos"], 0, 1)
        self.create_card(cards_frame, "Materiales", self.summary["materiales"], 0, 2)
        self.create_card(cards_frame, "Mano de Obra", self.summary["mano_obra"], 0, 3)

        self.create_card(cards_frame, "Herramientas", self.summary["herramientas"], 1, 0)
        self.create_card(cards_frame, "APUs", self.summary["apus"], 1, 1)
        self.create_card(cards_frame, "Presupuestos", self.summary["presupuestos"], 1, 2)
        self.create_card(
            cards_frame,
            "Valor Presupuestado",
            self.money(self.summary["valor_presupuestado"]),
            1,
            3
        )

        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)

        totals_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=12)
        totals_frame.pack(fill="x", padx=25, pady=15)

        ctk.CTkLabel(
            totals_frame,
            text="Resumen Financiero",
            font=("Arial", 18, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            totals_frame,
            text=f"Costo directo acumulado: {self.money(self.summary['costo_directo'])}",
            font=("Arial", 14, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=4)

        ctk.CTkLabel(
            totals_frame,
            text=f"Valor total presupuestado: {self.money(self.summary['valor_presupuestado'])}",
            font=("Arial", 15, "bold"),
            text_color=COLOR_TEXT
        ).pack(pady=(4, 15))

        table_title = ctk.CTkLabel(
            self,
            text="Últimos presupuestos registrados",
            font=("Arial", 18, "bold"),
            text_color=COLOR_TEXT
        )
        table_title.pack(pady=(10, 5))

        columns = [
            "codigo_presupuesto",
            "nombre_presupuesto",
            "nombre_proyecto",
            "valor_total_presupuesto",
            "estado"
        ]

        headings = {
            "codigo_presupuesto": "Código",
            "nombre_presupuesto": "Presupuesto",
            "nombre_proyecto": "Proyecto",
            "valor_total_presupuesto": "Valor Total",
            "estado": "Estado"
        }

        self.table = BaseTable(self, columns, headings)
        self.table.pack(expand=True, fill="both", padx=25, pady=10)

        presupuestos = self.summary["ultimos_presupuestos"]

        for item in presupuestos:
            item["valor_total_presupuesto"] = self.format_currency(
                item["valor_total_presupuesto"]
            )

        self.table.load_data(presupuestos)

    def create_card(self, master, title, value, row, column):
        card = ctk.CTkFrame(
            master,
            fg_color="#222222",
            corner_radius=12
        )
        card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 13, "bold"),
            text_color=COLOR_MUTED_TEXT
        ).pack(pady=(16, 4))

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 24, "bold"),
            text_color=COLOR_PRIMARY
        ).pack(pady=(0, 16))

    def money(self, value):
        try:
            return f"${float(value or 0):,.2f}"
        except Exception:
            return "$0.00"

    def format_currency(self, value):
        try:
            return (
                f"${float(value):,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
        except:
            return "$0,00"