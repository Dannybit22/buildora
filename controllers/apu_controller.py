from services.apu_service import ApuService


class ApuController:

    def __init__(self):
        self.service = ApuService()

    def load_apus(self):
        return self.service.get_all()

    def search_apus(self, text):
        return self.service.search(text)

    def get_apu(self, apu_id):
        return self.service.get_by_id(apu_id)

    def create_apu(self, data):
        return self.service.create_apu(data)

    def update_apu(self, apu_id, data):
        return self.service.update_apu(apu_id, data)

    def disable_apu(self, apu_id):
        return self.service.disable_apu(apu_id)

    def get_active_units(self):
        return self.service.get_active_units()

    def get_active_materials(self):
        return self.service.get_active_materials()

    def get_active_labor(self):
        return self.service.get_active_labor()

    def get_active_tools(self):
        return self.service.get_active_tools()

    def add_material(self, apu_id, material, cantidad):
        return self.service.add_material(apu_id, material, cantidad)

    def add_labor(self, apu_id, labor, cantidad):
        return self.service.add_labor(apu_id, labor, cantidad)

    def add_tool(self, apu_id, tool, cantidad):
        return self.service.add_tool(apu_id, tool, cantidad)

    def get_apu_materials(self, apu_id):
        return self.service.get_apu_materials(apu_id)

    def get_apu_labor(self, apu_id):
        return self.service.get_apu_labor(apu_id)

    def get_apu_tools(self, apu_id):
        return self.service.get_apu_tools(apu_id)

    def remove_material(self, apu_id, detail_id):
        return self.service.remove_material(apu_id, detail_id)

    def remove_labor(self, apu_id, detail_id):
        return self.service.remove_labor(apu_id, detail_id)

    def remove_tool(self, apu_id, detail_id):
        return self.service.remove_tool(apu_id, detail_id)