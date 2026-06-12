from repositories.cliente_repository import ClienteRepository


class ClienteService:

    def __init__(self):
        self.repository = ClienteRepository()

    def get_all(self):
        return self.repository.get_all()

    def search(self, text):
        return self.repository.search(text)

    def create(self, data):

        if not data["nombre_cliente"]:
            raise ValueError(
                "El nombre del cliente es obligatorio."
            )

        if not data["identificacion"]:
            raise ValueError(
                "La identificación es obligatoria."
            )

        return self.repository.create(data)

    def update(self, cliente_id, data):

        if not data["nombre_cliente"]:
            raise ValueError(
                "El nombre del cliente es obligatorio."
            )

        return self.repository.update(
            cliente_id,
            data
        )

    def disable(self, cliente_id):
        return self.repository.disable(cliente_id)

    def get_by_id(self, cliente_id):
        return self.repository.get_by_id(cliente_id)