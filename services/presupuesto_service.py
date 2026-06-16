from repositories.presupuesto_repository import (
    PresupuestoRepository,
    PresupuestoCapituloRepository,
    PresupuestoItemRepository
)


class PresupuestoService:

    def __init__(self):
        self.presupuesto_repo = PresupuestoRepository()
        self.capitulo_repo = PresupuestoCapituloRepository()
        self.item_repo = PresupuestoItemRepository()

    def get_all(self):
        return self.presupuesto_repo.get_all_with_project()

    def search(self, text):
        if not text:
            return self.get_all()
        return self.presupuesto_repo.search_with_project(text)

    def get_by_id(self, presupuesto_id):
        return self.presupuesto_repo.get_by_id_with_project(presupuesto_id)

    def get_projects(self):
        return self.presupuesto_repo.get_active_projects_without_budget()

    def get_all_projects(self):
        return self.presupuesto_repo.get_active_projects()

    def get_apus(self):
        return self.presupuesto_repo.get_active_apus()

    def create_budget(self, data):
        data = self.prepare_budget(data)
        self.validate_budget(data)
        return self.presupuesto_repo.create(data)

    def update_budget(self, presupuesto_id, data):
        data = self.prepare_budget(data)
        self.validate_budget(data)
        return self.presupuesto_repo.update(presupuesto_id, data)

    def close_budget(self, presupuesto_id):
        return self.presupuesto_repo.close_budget(presupuesto_id)

    def prepare_budget(self, data):
        return {
            "id_proyecto": data.get("id_proyecto"),
            "id_usuario_creador": data.get("id_usuario_creador"),
            "codigo_presupuesto": data.get("codigo_presupuesto", "").strip(),
            "nombre_presupuesto": data.get("nombre_presupuesto", "").strip(),
            "descripcion": data.get("descripcion", "").strip(),
            "fecha_presupuesto": data.get("fecha_presupuesto", "").strip(),
            "costo_directo_total": data.get("costo_directo_total", 0),
            "total_administracion": data.get("total_administracion", 0),
            "total_imprevistos": data.get("total_imprevistos", 0),
            "total_utilidad": data.get("total_utilidad", 0),
            "iva_utilidad": data.get("iva_utilidad", 0),
            "valor_total_presupuesto": data.get("valor_total_presupuesto", 0),
            "estado": data.get("estado", "borrador"),
            "observaciones": data.get("observaciones", "").strip()
        }

    def validate_budget(self, data):
        if not data.get("id_proyecto"):
            raise ValueError("Debe seleccionar un proyecto.")

        if not data.get("id_usuario_creador"):
            raise ValueError("No se encontró el usuario creador.")

        if not data.get("codigo_presupuesto"):
            raise ValueError("El código del presupuesto es obligatorio.")

        if not data.get("nombre_presupuesto"):
            raise ValueError("El nombre del presupuesto es obligatorio.")

        if not data.get("fecha_presupuesto"):
            raise ValueError("La fecha del presupuesto es obligatoria. Use formato AAAA-MM-DD.")

    def get_chapters(self, presupuesto_id):
        return self.capitulo_repo.get_by_budget(presupuesto_id)

    def create_chapter(self, data):
        data = self.prepare_chapter(data)
        self.validate_chapter(data)
        return self.capitulo_repo.create(data)

    def update_chapter(self, capitulo_id, data):
        data = self.prepare_chapter(data)
        self.validate_chapter(data)
        result = self.capitulo_repo.update(capitulo_id, data)
        self.recalculate_budget_by_chapter(capitulo_id)
        return result

    def disable_chapter(self, capitulo_id):
        chapter = self.capitulo_repo.get_by_id(capitulo_id)
        result = self.capitulo_repo.disable(capitulo_id)

        if chapter:
            self.recalculate_budget(chapter["id_presupuesto"])

        return result

    def prepare_chapter(self, data):
        return {
            "id_presupuesto": data.get("id_presupuesto"),
            "codigo_capitulo": data.get("codigo_capitulo", "").strip(),
            "nombre_capitulo": data.get("nombre_capitulo", "").strip(),
            "descripcion": data.get("descripcion", "").strip(),
            "orden": self.to_int(data.get("orden")) or 1,
            "costo_total_capitulo": data.get("costo_total_capitulo", 0),
            "porcentaje_participacion": data.get("porcentaje_participacion", 0),
            "estado": "activo"
        }

    def validate_chapter(self, data):
        if not data.get("id_presupuesto"):
            raise ValueError("Debe seleccionar un presupuesto.")

        if not data.get("codigo_capitulo"):
            raise ValueError("El código del capítulo es obligatorio.")

        if not data.get("nombre_capitulo"):
            raise ValueError("El nombre del capítulo es obligatorio.")

    def get_items_by_chapter(self, capitulo_id):
        return self.item_repo.get_by_chapter(capitulo_id)

    def get_items_by_budget(self, presupuesto_id):
        return self.item_repo.get_by_budget(presupuesto_id)

    def create_item_from_apu(self, data):
        data = self.prepare_item(data)
        self.validate_item(data)

        apu = self.item_repo.get_apu_snapshot(data["id_apu"])

        if not apu:
            raise ValueError("No se encontró el APU seleccionado.")

        cantidad = self.to_float(data.get("cantidad"))

        costo_unitario = self.to_float(apu.get("costo_directo_total"))
        costo_total = cantidad * costo_unitario

        item_data = {
            "id_capitulo": data["id_capitulo"],
            "id_apu": data["id_apu"],
            "codigo_item": data["codigo_item"],
            "descripcion_item": data["descripcion_item"],
            "unidad_item": data.get("unidad_item") or apu.get("codigo_unidad"),
            "cantidad": round(cantidad, 4),
            "costo_unitario_historico": round(costo_unitario, 2),
            "costo_total_item": round(costo_total, 2),
            "codigo_apu_historico": apu.get("codigo_apu"),
            "descripcion_apu_historica": apu.get("descripcion"),
            "unidad_apu_historica": apu.get("codigo_unidad"),
            "subtotal_materiales_historico": round(self.to_float(apu.get("subtotal_materiales")), 2),
            "subtotal_mano_obra_historico": round(self.to_float(apu.get("subtotal_mano_obra")), 2),
            "subtotal_herramientas_historico": round(self.to_float(apu.get("subtotal_herramientas")), 2),
            "orden": data["orden"],
            "estado": "activo"
        }

        item_id = self.item_repo.create(item_data)

        chapter = self.capitulo_repo.get_by_id(data["id_capitulo"])

        if chapter:
            self.recalculate_chapter(data["id_capitulo"])
            self.recalculate_budget(chapter["id_presupuesto"])

        return item_id

    def update_item_quantity(self, item_id, data):
        item = self.item_repo.get_by_id(item_id)

        if not item:
            raise ValueError("No se encontró el ítem.")

        cantidad = self.to_float(data.get("cantidad"))

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        costo_unitario = self.to_float(item.get("costo_unitario_historico"))
        costo_total = cantidad * costo_unitario

        update_data = {
            "id_capitulo": item["id_capitulo"],
            "id_apu": item["id_apu"],
            "codigo_item": item["codigo_item"],
            "descripcion_item": item["descripcion_item"],
            "unidad_item": item["unidad_item"],
            "cantidad": round(cantidad, 4),
            "costo_unitario_historico": item["costo_unitario_historico"],
            "costo_total_item": round(costo_total, 2),
            "codigo_apu_historico": item["codigo_apu_historico"],
            "descripcion_apu_historica": item["descripcion_apu_historica"],
            "unidad_apu_historica": item["unidad_apu_historica"],
            "subtotal_materiales_historico": item["subtotal_materiales_historico"],
            "subtotal_mano_obra_historico": item["subtotal_mano_obra_historico"],
            "subtotal_herramientas_historico": item["subtotal_herramientas_historico"],
            "orden": item["orden"],
            "estado": "activo"
        }

        result = self.item_repo.update(item_id, update_data)

        chapter = self.capitulo_repo.get_by_id(item["id_capitulo"])

        if chapter:
            self.recalculate_chapter(item["id_capitulo"])
            self.recalculate_budget(chapter["id_presupuesto"])

        return result

    def disable_item(self, item_id):
        item = self.item_repo.get_by_id(item_id)

        result = self.item_repo.disable(item_id)

        if item:
            chapter = self.capitulo_repo.get_by_id(item["id_capitulo"])

            if chapter:
                self.recalculate_chapter(item["id_capitulo"])
                self.recalculate_budget(chapter["id_presupuesto"])

        return result

    def prepare_item(self, data):
        return {
            "id_capitulo": data.get("id_capitulo"),
            "id_apu": data.get("id_apu"),
            "codigo_item": data.get("codigo_item", "").strip(),
            "descripcion_item": data.get("descripcion_item", "").strip(),
            "unidad_item": data.get("unidad_item", "").strip(),
            "cantidad": self.to_float(data.get("cantidad")),
            "orden": self.to_int(data.get("orden")) or 1
        }

    def validate_item(self, data):
        if not data.get("id_capitulo"):
            raise ValueError("Debe seleccionar un capítulo.")

        if not data.get("id_apu"):
            raise ValueError("Debe seleccionar un APU.")

        if not data.get("codigo_item"):
            raise ValueError("El código del ítem es obligatorio.")

        if not data.get("descripcion_item"):
            raise ValueError("La descripción del ítem es obligatoria.")

        if data.get("cantidad", 0) <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    def recalculate_chapter(self, capitulo_id):
        total = self.item_repo.sum_chapter_items(capitulo_id)
        self.capitulo_repo.update_total(capitulo_id, round(total, 2))
        return total

    def recalculate_budget_by_chapter(self, capitulo_id):
        chapter = self.capitulo_repo.get_by_id(capitulo_id)

        if chapter:
            return self.recalculate_budget(chapter["id_presupuesto"])

        return None

    def recalculate_budget(self, presupuesto_id):
        costo_directo = self.item_repo.sum_budget_items(presupuesto_id)

        budget = self.presupuesto_repo.get_by_id(presupuesto_id)

        if not budget:
            return None

        total_administracion = self.to_float(budget.get("total_administracion"))
        total_imprevistos = self.to_float(budget.get("total_imprevistos"))
        total_utilidad = self.to_float(budget.get("total_utilidad"))
        iva_utilidad = self.to_float(budget.get("iva_utilidad"))

        valor_total = (
            costo_directo
            + total_administracion
            + total_imprevistos
            + total_utilidad
            + iva_utilidad
        )

        data = {
            "id_proyecto": budget["id_proyecto"],
            "id_usuario_creador": budget["id_usuario_creador"],
            "codigo_presupuesto": budget["codigo_presupuesto"],
            "nombre_presupuesto": budget["nombre_presupuesto"],
            "descripcion": budget["descripcion"],
            "fecha_presupuesto": budget["fecha_presupuesto"],
            "costo_directo_total": round(costo_directo, 2),
            "total_administracion": round(total_administracion, 2),
            "total_imprevistos": round(total_imprevistos, 2),
            "total_utilidad": round(total_utilidad, 2),
            "iva_utilidad": round(iva_utilidad, 2),
            "valor_total_presupuesto": round(valor_total, 2),
            "estado": budget["estado"],
            "observaciones": budget["observaciones"]
        }

        self.presupuesto_repo.update(presupuesto_id, data)
        self.recalculate_chapter_percentages(presupuesto_id, costo_directo)

        return data

    def recalculate_chapter_percentages(self, presupuesto_id, costo_directo):
        chapters = self.capitulo_repo.get_by_budget(presupuesto_id)

        for chapter in chapters:
            total_capitulo = self.to_float(chapter.get("costo_total_capitulo"))
            porcentaje = 0

            if costo_directo > 0:
                porcentaje = (total_capitulo / costo_directo) * 100

            self.capitulo_repo.update_percentage(
                chapter["id_capitulo"],
                round(porcentaje, 4)
            )

    def to_float(self, value):
        try:
            if value is None or value == "":
                return 0
            return float(str(value).replace(",", "."))
        except Exception:
            return 0

    def to_int(self, value):
        try:
            if value is None or value == "":
                return 0
            return int(float(str(value).replace(",", ".")))
        except Exception:
            return 0