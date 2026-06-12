from services.cliente_service import ClienteService


class ClienteController:

    def __init__(self):
        self.service = ClienteService()

    def load_clients(self):
        return self.service.get_all()

    def search_clients(self, text):
        return self.service.search(text)

    def create_client(self, data):
        return self.service.create(data)

    def update_client(self, cliente_id, data):
        return self.service.update(cliente_id, data)

    def disable_client(self, cliente_id):
        return self.service.disable(cliente_id)

    def get_client(self, cliente_id):
        return self.service.get_by_id(cliente_id)