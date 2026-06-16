from services.proyecto_service import ProyectoService


class ProyectoController:

    def __init__(self):
        self.service = ProyectoService()

    def load_projects(self):
        return self.service.get_all()

    def search_projects(self, text):
        return self.service.search(text)

    def get_project(self, proyecto_id):
        return self.service.get_by_id(proyecto_id)

    def create_project(self, data):
        return self.service.create(data)

    def update_project(self, proyecto_id, data):
        return self.service.update(proyecto_id, data)

    def disable_project(self, proyecto_id):
        return self.service.disable(proyecto_id)

    def get_active_clients(self):
        return self.service.get_active_clients()