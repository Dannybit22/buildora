from repositories.proyecto_repository import ProyectoRepository


class ProyectoService:

    def __init__(self):
        self.repository = ProyectoRepository()

    def get_all(self):
        return self.repository.get_all_with_client()

    def search(self, text):
        if not text:
            return self.get_all()

        return self.repository.search_with_client(text)

    def get_by_id(self, proyecto_id):
        return self.repository.get_by_id_with_client(proyecto_id)

    def get_active_clients(self):
        return self.repository.get_active_clients()

    def create(self, data):
        self.validate(data)
        return self.repository.create(data)

    def update(self, proyecto_id, data):
        self.validate(data)
        return self.repository.update(proyecto_id, data)

    def disable(self, proyecto_id):
        return self.repository.disable(proyecto_id)

    def validate(self, data):
        if not data.get("id_cliente"):
            raise ValueError("Debe seleccionar un cliente.")

        if not data.get("codigo_proyecto"):
            raise ValueError("El código del proyecto es obligatorio.")

        if not data.get("nombre_proyecto"):
            raise ValueError("El nombre del proyecto es obligatorio.")

        if not data.get("fecha_proyecto"):
            raise ValueError("La fecha del proyecto es obligatoria. Use formato AAAA-MM-DD.")