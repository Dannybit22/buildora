from services.aiu_service import AiuService


class AiuController:

    def __init__(self):
        self.service = AiuService()

    def get_active_budgets(self):
        return self.service.get_active_budgets()

    def get_budget(self, presupuesto_id):
        return self.service.get_budget(presupuesto_id)

    def get_administracion(self, presupuesto_id):
        return self.service.get_administracion(presupuesto_id)

    def get_imprevistos(self, presupuesto_id):
        return self.service.get_imprevistos(presupuesto_id)

    def get_utilidad(self, presupuesto_id):
        return self.service.get_utilidad(presupuesto_id)

    def save_administracion(self, presupuesto_id, data):
        return self.service.save_administracion(presupuesto_id, data)

    def save_imprevistos(self, presupuesto_id, data):
        return self.service.save_imprevistos(presupuesto_id, data)

    def save_utilidad(self, presupuesto_id, data):
        return self.service.save_utilidad(presupuesto_id, data)

    def recalculate_aiu(self, presupuesto_id):
        return self.service.recalculate_aiu(presupuesto_id)