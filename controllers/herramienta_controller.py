from services.herramienta_service import HerramientaService


class HerramientaController:

    def __init__(self):
        self.service = HerramientaService()

    def load_tools(self):
        return self.service.get_all()

    def search_tools(self, text):
        return self.service.search(text)

    def get_tool(self, herramienta_id):
        return self.service.get_by_id(herramienta_id)

    def create_tool(self, data):
        return self.service.create(data)

    def update_tool(self, herramienta_id, data):
        return self.service.update(
            herramienta_id,
            data
        )

    def disable_tool(self, herramienta_id):
        return self.service.disable(
            herramienta_id
        )

    def get_active_categories(self):
        return self.service.get_active_categories()

    def get_active_units(self):
        return self.service.get_active_units()