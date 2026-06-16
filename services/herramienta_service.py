from repositories.herramienta_repository import HerramientaRepository


class HerramientaService:

    def __init__(self):
        self.repository = HerramientaRepository()

    def get_all(self):
        return self.repository.get_all_with_relations()

    def search(self, text):

        if not text:
            return self.get_all()

        return self.repository.search_with_relations(text)

    def get_by_id(self, herramienta_id):
        return self.repository.get_by_id_with_relations(herramienta_id)

    def get_active_categories(self):
        return self.repository.get_active_categories()

    def get_active_units(self):
        return self.repository.get_active_units()

    def create(self, data):

        data = self.prepare_data(data)

        self.validate(data)

        return self.repository.create(data)

    def update(self, herramienta_id, data):

        data = self.prepare_data(data)

        self.validate(data)

        return self.repository.update(
            herramienta_id,
            data
        )

    def disable(self, herramienta_id):
        return self.repository.disable(herramienta_id)

    def prepare_data(self, data):

        valor_comercial = self.to_float(
            data.get("valor_comercial")
        )

        rendimiento = self.to_float(
            data.get("rendimiento")
        )

        numero_herramientas = self.to_float(
            data.get("numero_herramientas_obra")
        )

        if rendimiento <= 0:
            rendimiento = 1

        if numero_herramientas <= 0:
            numero_herramientas = 1

        valor_hora = valor_comercial * rendimiento

        valor_por_obra = (
            valor_hora *
            numero_herramientas
        )

        return {
            "id_categoria_herramienta":
                data.get("id_categoria_herramienta"),

            "id_unidad":
                data.get("id_unidad"),

            "codigo_herramienta":
                data.get("codigo_herramienta", "").strip(),

            "nombre_herramienta":
                data.get("nombre_herramienta", "").strip(),

            "valor_comercial":
                round(valor_comercial, 4),

            "rendimiento":
                round(rendimiento, 4),

            "numero_herramientas_obra":
                round(numero_herramientas, 4),

            "valor_hora":
                round(valor_hora, 4),

            "valor_por_obra":
                round(valor_por_obra, 4),

            "estado":
                "activo"
        }

    def validate(self, data):

        if not data.get("id_categoria_herramienta"):
            raise ValueError(
                "Debe seleccionar una categoría."
            )

        if not data.get("id_unidad"):
            raise ValueError(
                "Debe seleccionar una unidad."
            )

        if not data.get("codigo_herramienta"):
            raise ValueError(
                "El código es obligatorio."
            )

        if not data.get("nombre_herramienta"):
            raise ValueError(
                "El nombre es obligatorio."
            )

        if data.get("valor_comercial", 0) <= 0:
            raise ValueError(
                "El valor comercial debe ser mayor que cero."
            )

        if data.get("rendimiento", 0) <= 0:
            raise ValueError(
                "El rendimiento debe ser mayor que cero."
            )

        if data.get("numero_herramientas_obra", 0) <= 0:
            raise ValueError(
                "El número de herramientas debe ser mayor que cero."
            )

    def to_float(self, value):

        try:

            if value is None:
                return 0

            if value == "":
                return 0

            return float(
                str(value).replace(",", ".")
            )

        except:
            return 0