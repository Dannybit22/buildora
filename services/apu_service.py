from repositories.apu_repository import ApuRepository


class ApuService:

    def __init__(self):
        self.repository = ApuRepository()

    def get_all(self):
        return self.repository.get_all_with_unit()

    def search(self, text):
        if not text:
            return self.get_all()
        return self.repository.search_with_unit(text)

    def get_by_id(self, apu_id):
        return self.repository.get_by_id_with_unit(apu_id)

    def get_active_units(self):
        return self.repository.get_active_units()

    def get_active_materials(self):
        return self.repository.get_active_materials()

    def get_active_labor(self):
        return self.repository.get_active_labor()

    def get_active_tools(self):
        return self.repository.get_active_tools()

    def create_apu(self, data):
        data = self.prepare_header(data)
        self.validate_header(data)
        return self.repository.create(data)

    def update_apu(self, apu_id, data):
        data = self.prepare_header(data)
        self.validate_header(data)
        return self.repository.update(apu_id, data)

    def disable_apu(self, apu_id):
        return self.repository.disable(apu_id)

    def prepare_header(self, data):
        return {
            "id_unidad": data.get("id_unidad"),
            "codigo_apu": data.get("codigo_apu", "").strip(),
            "descripcion": data.get("descripcion", "").strip(),
            "cantidad_base": self.to_float(data.get("cantidad_base")) or 1,
            "subtotal_materiales": data.get("subtotal_materiales", 0),
            "subtotal_mano_obra": data.get("subtotal_mano_obra", 0),
            "subtotal_herramientas": data.get("subtotal_herramientas", 0),
            "costo_directo_total": data.get("costo_directo_total", 0),
            "porcentaje_materiales": data.get("porcentaje_materiales", 0),
            "porcentaje_mano_obra": data.get("porcentaje_mano_obra", 0),
            "porcentaje_herramientas": data.get("porcentaje_herramientas", 0),
            "observaciones": data.get("observaciones", "").strip(),
            "estado": "activo"
        }

    def validate_header(self, data):
        if not data.get("id_unidad"):
            raise ValueError("Debe seleccionar una unidad de medida.")

        if not data.get("codigo_apu"):
            raise ValueError("El código del APU es obligatorio.")

        if not data.get("descripcion"):
            raise ValueError("La descripción del APU es obligatoria.")

        if data.get("cantidad_base", 0) <= 0:
            raise ValueError("La cantidad base debe ser mayor que cero.")

    def add_material(self, apu_id, material, cantidad):
        cantidad = self.to_float(cantidad)

        if not apu_id:
            raise ValueError("Debe seleccionar un APU.")

        if not material:
            raise ValueError("Debe seleccionar un material.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        valor_unitario = self.to_float(material.get("valor_total"))
        subtotal = cantidad * valor_unitario

        data = {
            "id_apu": apu_id,
            "id_material": material["id_material"],
            "descripcion_material": material["descripcion"],
            "unidad_material": material.get("unidad_cotizacion") or "",
            "cantidad": round(cantidad, 4),
            "valor_unitario": round(valor_unitario, 4),
            "subtotal": round(subtotal, 2)
        }

        result = self.repository.add_material(data)
        self.recalculate_totals(apu_id)
        return result

    def add_labor(self, apu_id, labor, cantidad):
        cantidad = self.to_float(cantidad)

        if not apu_id:
            raise ValueError("Debe seleccionar un APU.")

        if not labor:
            raise ValueError("Debe seleccionar una mano de obra.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        valor_unitario = self.to_float(labor.get("costo_dia"))
        subtotal = cantidad * valor_unitario

        data = {
            "id_apu": apu_id,
            "id_mano_obra": labor["id_mano_obra"],
            "nombre_cargo": labor["nombre_cargo"],
            "unidad_mano_obra": "DIA",
            "cantidad": round(cantidad, 4),
            "valor_unitario": round(valor_unitario, 4),
            "subtotal": round(subtotal, 2)
        }

        result = self.repository.add_labor(data)
        self.recalculate_totals(apu_id)
        return result

    def add_tool(self, apu_id, tool, cantidad):
        cantidad = self.to_float(cantidad)

        if not apu_id:
            raise ValueError("Debe seleccionar un APU.")

        if not tool:
            raise ValueError("Debe seleccionar una herramienta.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        valor_unitario = self.to_float(tool.get("valor_por_obra"))
        subtotal = cantidad * valor_unitario

        data = {
            "id_apu": apu_id,
            "id_herramienta": tool["id_herramienta"],
            "nombre_herramienta": tool["nombre_herramienta"],
            "unidad_herramienta": "UND",
            "cantidad": round(cantidad, 4),
            "valor_unitario": round(valor_unitario, 4),
            "subtotal": round(subtotal, 2)
        }

        result = self.repository.add_tool(data)
        self.recalculate_totals(apu_id)
        return result

    def get_apu_materials(self, apu_id):
        return self.repository.get_apu_materials(apu_id)

    def get_apu_labor(self, apu_id):
        return self.repository.get_apu_labor(apu_id)

    def get_apu_tools(self, apu_id):
        return self.repository.get_apu_tools(apu_id)

    def remove_material(self, apu_id, detail_id):
        result = self.repository.disable_material_detail(detail_id)
        self.recalculate_totals(apu_id)
        return result

    def remove_labor(self, apu_id, detail_id):
        result = self.repository.disable_labor_detail(detail_id)
        self.recalculate_totals(apu_id)
        return result

    def remove_tool(self, apu_id, detail_id):
        result = self.repository.disable_tool_detail(detail_id)
        self.recalculate_totals(apu_id)
        return result

    def recalculate_totals(self, apu_id):
        materials = self.repository.get_apu_materials(apu_id)
        labor = self.repository.get_apu_labor(apu_id)
        tools = self.repository.get_apu_tools(apu_id)

        subtotal_materiales = sum(
            self.to_float(item.get("subtotal"))
            for item in materials
        )

        subtotal_mano_obra = sum(
            self.to_float(item.get("subtotal"))
            for item in labor
        )

        subtotal_herramientas = sum(
            self.to_float(item.get("subtotal"))
            for item in tools
        )

        total = (
            subtotal_materiales
            + subtotal_mano_obra
            + subtotal_herramientas
        )

        porcentaje_materiales = 0
        porcentaje_mano_obra = 0
        porcentaje_herramientas = 0

        if total > 0:
            porcentaje_materiales = (
                subtotal_materiales / total
            ) * 100

            porcentaje_mano_obra = (
                subtotal_mano_obra / total
            ) * 100

            porcentaje_herramientas = (
                subtotal_herramientas / total
            ) * 100

        totals = {
            "subtotal_materiales": round(subtotal_materiales, 2),
            "subtotal_mano_obra": round(subtotal_mano_obra, 2),
            "subtotal_herramientas": round(subtotal_herramientas, 2),
            "costo_directo_total": round(total, 2),
            "porcentaje_materiales": round(porcentaje_materiales, 4),
            "porcentaje_mano_obra": round(porcentaje_mano_obra, 4),
            "porcentaje_herramientas": round(porcentaje_herramientas, 4)
        }

        self.repository.update_totals(apu_id, totals)

        return totals

    def to_float(self, value):
        try:
            if value is None or value == "":
                return 0
            return float(str(value).replace(",", "."))
        except Exception:
            return 0