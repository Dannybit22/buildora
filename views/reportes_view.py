import os
import customtkinter as ctk

from controllers.reportes_controller import ReportesController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class ReportesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = ReportesController()
        self.selected_presupuesto_id = None

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Reportes Buildora",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            button_frame,
            text="Exportar Presupuesto a Excel",
            command=self.export_excel
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Exportar Presupuesto a PDF",
            command=self.export_pdf
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Recargar",
            command=self.load_data
        ).pack(side="left", padx=5)

        columns = [
            "id_presupuesto",
            "codigo_presupuesto",
            "nombre_presupuesto",
            "nombre_proyecto",
            "nombre_cliente",
            "fecha_presupuesto",
            "costo_directo_total",
            "valor_total_presupuesto",
            "estado"
        ]

        headings = {
            "id_presupuesto": "ID",
            "codigo_presupuesto": "Código",
            "nombre_presupuesto": "Presupuesto",
            "nombre_proyecto": "Proyecto",
            "nombre_cliente": "Cliente",
            "fecha_presupuesto": "Fecha",
            "costo_directo_total": "Costo Directo",
            "valor_total_presupuesto": "Total",
            "estado": "Estado"
        }

        self.table = BaseTable(self, columns, headings)
        self.table.pack(expand=True, fill="both", padx=10, pady=10)

        self.table.tree.bind("<<TreeviewSelect>>", self.on_select)

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


    def format_money_fields(self, data):
        money_fields = [
            "costo_directo_total",
            "valor_total_presupuesto"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data    
        
    def load_data(self):
        data = self.controller.get_presupuestos()
        data = self.format_money_fields(data)

        self.table.load_data(data)

    def on_select(self, event):
        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_presupuesto_id = values[0]

    def export_excel(self):
        if not self.selected_presupuesto_id:
            MessageUtils.warning("Seleccione un presupuesto.")
            return

        try:
            filepath = self.controller.generar_excel_presupuesto(
                self.selected_presupuesto_id
            )

            MessageUtils.success(
                f"Reporte Excel generado correctamente:\n{filepath}"
            )

            try:
                os.startfile(filepath)
            except Exception:
                pass

        except Exception as error:
            MessageUtils.error(str(error))

    def export_pdf(self):
        if not self.selected_presupuesto_id:
            MessageUtils.warning("Seleccione un presupuesto.")
            return

        try:
            filepath = self.controller.generar_pdf_presupuesto(
                self.selected_presupuesto_id
            )

            MessageUtils.success(
                f"Reporte PDF generado correctamente:\n{filepath}"
            )

            try:
                os.startfile(filepath)
            except Exception:
                pass

        except Exception as error:
            MessageUtils.error(str(error))