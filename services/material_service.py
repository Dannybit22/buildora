from repositories.material_repository import MaterialRepository


class MaterialService:

    def __init__(self):
        self.repository = MaterialRepository()

    def get_all(self):
        return self.repository.get_all_with_relations()

    def search(self, text):
        if not text:
            return self.get_all()
        return self.repository.search_with_relations(text)

    def get_by_id(self, material_id):
        return self.repository.get_by_id_with_relations(material_id)

    def get_active_categories(self):
        return self.repository.get_active_categories()

    def get_active_units(self):
        return self.repository.get_active_units()

    def create(self, data):
        data = self.prepare_data(data)
        self.validate(data)
        return self.repository.create(data)

    def update(self, material_id, data):
        data = self.prepare_data(data)
        self.validate(data)
        return self.repository.update(material_id, data)

    def disable(self, material_id):
        return self.repository.disable(material_id)

    def prepare_data(self, data):
        valor_comercial = self.to_float(data.get("valor_comercial_empaque"))
        cantidad_empaque = self.to_float(data.get("cantidad_por_empaque"))
        rendimiento = self.to_float(data.get("rendimiento"))
        desperdicio = self.to_float(data.get("porcentaje_desperdicio"))

        if cantidad_empaque <= 0:
            cantidad_empaque = 1

        if rendimiento <= 0:
            rendimiento = 1

        precio_por_unidad = valor_comercial / cantidad_empaque
        valor_por_unidad_cotizacion = precio_por_unidad * rendimiento
        valor_desperdicio = valor_por_unidad_cotizacion * (desperdicio / 100)
        valor_total = valor_por_unidad_cotizacion + valor_desperdicio

        return {
            "id_categoria_material": data.get("id_categoria_material"),
            "id_unidad": data.get("id_unidad"),
            "codigo_material": data.get("codigo_material", "").strip(),
            "descripcion": data.get("descripcion", "").strip(),
            "valor_comercial_empaque": valor_comercial,
            "cantidad_por_empaque": cantidad_empaque,
            "precio_por_unidad": round(precio_por_unidad, 4),
            "rendimiento": rendimiento,
            "unidad_cotizacion": data.get("unidad_cotizacion", "").strip(),
            "valor_por_unidad_cotizacion": round(valor_por_unidad_cotizacion, 4),
            "porcentaje_desperdicio": desperdicio,
            "valor_desperdicio": round(valor_desperdicio, 4),
            "valor_total": round(valor_total, 4),
            "estado": "activo"
        }

    def validate(self, data):
        if not data.get("id_unidad"):
            raise ValueError("Debe seleccionar una unidad de medida.")

        if not data.get("codigo_material"):
            raise ValueError("El código del material es obligatorio.")

        if not data.get("descripcion"):
            raise ValueError("La descripción del material es obligatoria.")

        if data.get("valor_comercial_empaque", 0) < 0:
            raise ValueError("El valor comercial no puede ser negativo.")

        if data.get("cantidad_por_empaque", 0) <= 0:
            raise ValueError("La cantidad por empaque debe ser mayor que cero.")

        if data.get("rendimiento", 0) <= 0:
            raise ValueError("El rendimiento debe ser mayor que cero.")

        if data.get("porcentaje_desperdicio", 0) < 0:
            raise ValueError("El porcentaje de desperdicio no puede ser negativo.")

    def to_float(self, value):
        try:
            if value is None or value == "":
                return 0
            return float(str(value).replace(",", "."))
        except Exception:
            return 0