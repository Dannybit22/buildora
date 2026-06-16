from services.reportes_service import ReportesService


class ReportesController:

    def __init__(self):
        self.service = ReportesService()

    def get_presupuestos(self):
        return self.service.get_presupuestos()

    def generar_excel_presupuesto(self, presupuesto_id):
        return self.service.generar_excel_presupuesto(presupuesto_id)

    def generar_pdf_presupuesto(self, presupuesto_id):
        return self.service.generar_pdf_presupuesto(presupuesto_id)