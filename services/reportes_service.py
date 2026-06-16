import os
from datetime import datetime

from repositories.presupuesto_repository import (
    PresupuestoRepository,
    PresupuestoCapituloRepository,
    PresupuestoItemRepository
)
from reports.presupuesto_excel import PresupuestoExcelReport
from reports.presupuesto_pdf import PresupuestoPdfReport


class ReportesService:

    def __init__(self):
        self.presupuesto_repo = PresupuestoRepository()
        self.capitulo_repo = PresupuestoCapituloRepository()
        self.item_repo = PresupuestoItemRepository()

    def get_presupuestos(self):
        return self.presupuesto_repo.get_all_with_project()

    def get_report_data(self, presupuesto_id):
        presupuesto = self.presupuesto_repo.get_by_id_with_project(presupuesto_id)

        if not presupuesto:
            raise ValueError("No se encontró el presupuesto seleccionado.")

        capitulos = self.capitulo_repo.get_by_budget(presupuesto_id)
        items = self.item_repo.get_by_budget(presupuesto_id)

        return presupuesto, capitulos, items

    def get_output_filename(self, presupuesto, extension):
        output_dir = "exports"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return os.path.join(
            output_dir,
            f"Presupuesto_{presupuesto['codigo_presupuesto']}_{timestamp}.{extension}"
        )

    def generar_excel_presupuesto(self, presupuesto_id):
        presupuesto, capitulos, items = self.get_report_data(presupuesto_id)

        filename = self.get_output_filename(presupuesto, "xlsx")

        report = PresupuestoExcelReport(
            presupuesto=presupuesto,
            capitulos=capitulos,
            items=items
        )

        return report.generate(filename)

    def generar_pdf_presupuesto(self, presupuesto_id):
        presupuesto, capitulos, items = self.get_report_data(presupuesto_id)

        filename = self.get_output_filename(presupuesto, "pdf")

        report = PresupuestoPdfReport(
            presupuesto=presupuesto,
            capitulos=capitulos,
            items=items
        )

        return report.generate(filename)