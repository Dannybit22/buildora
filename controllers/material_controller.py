from services.material_service import MaterialService


class MaterialController:

    def __init__(self):
        self.service = MaterialService()

    def load_materials(self):
        return self.service.get_all()

    def search_materials(self, text):
        return self.service.search(text)

    def get_material(self, material_id):
        return self.service.get_by_id(material_id)

    def create_material(self, data):
        return self.service.create(data)

    def update_material(self, material_id, data):
        return self.service.update(material_id, data)

    def disable_material(self, material_id):
        return self.service.disable(material_id)

    def get_active_categories(self):
        return self.service.get_active_categories()

    def get_active_units(self):
        return self.service.get_active_units()