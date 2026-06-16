from services.presupuesto_service import PresupuestoService


class PresupuestoController:

    def __init__(self):
        self.service = PresupuestoService()

    def load_budgets(self):
        return self.service.get_all()

    def search_budgets(self, text):
        return self.service.search(text)

    def get_budget(self, presupuesto_id):
        return self.service.get_by_id(presupuesto_id)

    def get_projects(self):
        return self.service.get_projects()

    def get_all_projects(self):
        return self.service.get_all_projects()

    def get_apus(self):
        return self.service.get_apus()

    def create_budget(self, data):
        return self.service.create_budget(data)

    def update_budget(self, presupuesto_id, data):
        return self.service.update_budget(presupuesto_id, data)

    def close_budget(self, presupuesto_id):
        return self.service.close_budget(presupuesto_id)

    def get_chapters(self, presupuesto_id):
        return self.service.get_chapters(presupuesto_id)

    def create_chapter(self, data):
        return self.service.create_chapter(data)

    def update_chapter(self, capitulo_id, data):
        return self.service.update_chapter(capitulo_id, data)

    def disable_chapter(self, capitulo_id):
        return self.service.disable_chapter(capitulo_id)

    def get_items_by_chapter(self, capitulo_id):
        return self.service.get_items_by_chapter(capitulo_id)

    def get_items_by_budget(self, presupuesto_id):
        return self.service.get_items_by_budget(presupuesto_id)

    def create_item_from_apu(self, data):
        return self.service.create_item_from_apu(data)

    def update_item_quantity(self, item_id, data):
        return self.service.update_item_quantity(item_id, data)

    def disable_item(self, item_id):
        return self.service.disable_item(item_id)