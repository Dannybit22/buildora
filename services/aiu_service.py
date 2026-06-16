from repositories.aiu_repository import AiuRepository


class AiuService:

    def __init__(self):
        self.repository = AiuRepository()

    def get_active_budgets(self):
        return self.repository.get_active_budgets()

    def get_budget(self, presupuesto_id):
        return self.repository.get_budget(presupuesto_id)

    def get_administracion(self, presupuesto_id):
        return self.repository.get_administracion(presupuesto_id)

    def get_imprevistos(self, presupuesto_id):
        return self.repository.get_imprevistos(presupuesto_id)

    def get_utilidad(self, presupuesto_id):
        return self.repository.get_utilidad(presupuesto_id)

    def save_administracion(self, presupuesto_id, data):
        budget = self.repository.get_budget(presupuesto_id)

        if not budget:
            raise ValueError("No se encontró el presupuesto.")

        costo_directo = self.to_float(budget.get("costo_directo_total"))

        total = (
            self.to_float(data.get("total_personal_tecnico"))
            + self.to_float(data.get("total_personal_administrativo"))
            + self.to_float(data.get("total_ocupacional"))
            + self.to_float(data.get("total_dotacion_oficina"))
            + self.to_float(data.get("total_equipos"))
            + self.to_float(data.get("total_caja_menor"))
            + self.to_float(data.get("total_garantias"))
            + self.to_float(data.get("total_impuestos"))
        )

        porcentaje = 0
        if costo_directo > 0:
            porcentaje = (total / costo_directo) * 100

        admin_data = {
            "id_presupuesto": presupuesto_id,
            "total_personal_tecnico": self.to_float(data.get("total_personal_tecnico")),
            "total_personal_administrativo": self.to_float(data.get("total_personal_administrativo")),
            "total_ocupacional": self.to_float(data.get("total_ocupacional")),
            "total_dotacion_oficina": self.to_float(data.get("total_dotacion_oficina")),
            "total_equipos": self.to_float(data.get("total_equipos")),
            "total_caja_menor": self.to_float(data.get("total_caja_menor")),
            "total_garantias": self.to_float(data.get("total_garantias")),
            "total_impuestos": self.to_float(data.get("total_impuestos")),
            "total_administracion": round(total, 2),
            "porcentaje_administracion": round(porcentaje, 4),
            "observaciones": data.get("observaciones", "").strip()
        }

        self.repository.save_administracion(admin_data)
        self.recalculate_aiu(presupuesto_id)

        return admin_data

    def save_imprevistos(self, presupuesto_id, data):
        budget = self.repository.get_budget(presupuesto_id)

        if not budget:
            raise ValueError("No se encontró el presupuesto.")

        costo_directo = self.to_float(budget.get("costo_directo_total"))

        total = (
            self.to_float(data.get("total_imprevisto_mano_obra"))
            + self.to_float(data.get("total_imprevisto_materiales"))
            + self.to_float(data.get("total_imprevisto_riesgo"))
            + self.to_float(data.get("total_imprevisto_administracion"))
        )

        porcentaje = 0
        if costo_directo > 0:
            porcentaje = (total / costo_directo) * 100

        imp_data = {
            "id_presupuesto": presupuesto_id,
            "total_imprevisto_mano_obra": self.to_float(data.get("total_imprevisto_mano_obra")),
            "total_imprevisto_materiales": self.to_float(data.get("total_imprevisto_materiales")),
            "total_imprevisto_riesgo": self.to_float(data.get("total_imprevisto_riesgo")),
            "total_imprevisto_administracion": self.to_float(data.get("total_imprevisto_administracion")),
            "total_imprevistos": round(total, 2),
            "porcentaje_imprevistos": round(porcentaje, 4),
            "observaciones": data.get("observaciones", "").strip()
        }

        self.repository.save_imprevistos(imp_data)
        self.recalculate_aiu(presupuesto_id)

        return imp_data

    def save_utilidad(self, presupuesto_id, data):
        budget = self.repository.get_budget(presupuesto_id)

        if not budget:
            raise ValueError("No se encontró el presupuesto.")

        costo_directo = self.to_float(budget.get("costo_directo_total"))

        porcentaje_utilidad = self.to_float(data.get("porcentaje_utilidad_operativa"))
        porcentaje_retefuente = self.to_float(data.get("porcentaje_retefuente"))
        porcentaje_renta = self.to_float(data.get("porcentaje_renta"))
        porcentaje_iva = self.to_float(data.get("porcentaje_iva_utilidad"))

        utilidad_operativa = costo_directo * (porcentaje_utilidad / 100)
        valor_retefuente = utilidad_operativa * (porcentaje_retefuente / 100)
        valor_renta = utilidad_operativa * (porcentaje_renta / 100)

        total_utilidad = utilidad_operativa - valor_retefuente - valor_renta
        iva_utilidad = total_utilidad * (porcentaje_iva / 100)

        util_data = {
            "id_presupuesto": presupuesto_id,
            "porcentaje_utilidad_operativa": round(porcentaje_utilidad, 4),
            "utilidad_operativa": round(utilidad_operativa, 2),
            "porcentaje_retefuente": round(porcentaje_retefuente, 4),
            "valor_retefuente": round(valor_retefuente, 2),
            "porcentaje_renta": round(porcentaje_renta, 4),
            "valor_renta": round(valor_renta, 2),
            "total_utilidad": round(total_utilidad, 2),
            "porcentaje_iva_utilidad": round(porcentaje_iva, 4),
            "iva_utilidad": round(iva_utilidad, 2),
            "observaciones": data.get("observaciones", "").strip()
        }

        self.repository.save_utilidad(util_data)
        self.recalculate_aiu(presupuesto_id)

        return util_data

    def recalculate_aiu(self, presupuesto_id):
        budget = self.repository.get_budget(presupuesto_id)

        if not budget:
            raise ValueError("No se encontró el presupuesto.")

        admin = self.repository.get_administracion(presupuesto_id) or {}
        imp = self.repository.get_imprevistos(presupuesto_id) or {}
        util = self.repository.get_utilidad(presupuesto_id) or {}

        costo_directo = self.to_float(budget.get("costo_directo_total"))

        total_administracion = self.to_float(admin.get("total_administracion"))
        porcentaje_administracion = self.to_float(admin.get("porcentaje_administracion"))

        total_imprevistos = self.to_float(imp.get("total_imprevistos"))
        porcentaje_imprevistos = self.to_float(imp.get("porcentaje_imprevistos"))

        total_utilidad = self.to_float(util.get("total_utilidad"))
        porcentaje_utilidad = self.to_float(util.get("porcentaje_utilidad_operativa"))

        iva_utilidad = self.to_float(util.get("iva_utilidad"))
        porcentaje_iva_utilidad = self.to_float(util.get("porcentaje_iva_utilidad"))

        total_aiu = (
            total_administracion
            + total_imprevistos
            + total_utilidad
            + iva_utilidad
        )

        porcentaje_total_aiu = 0
        if costo_directo > 0:
            porcentaje_total_aiu = (total_aiu / costo_directo) * 100

        valor_total_presupuesto = costo_directo + total_aiu

        aiu_data = {
            "id_presupuesto": presupuesto_id,
            "costo_directo_total": round(costo_directo, 2),
            "total_administracion": round(total_administracion, 2),
            "porcentaje_administracion": round(porcentaje_administracion, 4),
            "total_imprevistos": round(total_imprevistos, 2),
            "porcentaje_imprevistos": round(porcentaje_imprevistos, 4),
            "total_utilidad": round(total_utilidad, 2),
            "porcentaje_utilidad": round(porcentaje_utilidad, 4),
            "iva_utilidad": round(iva_utilidad, 2),
            "porcentaje_iva_utilidad": round(porcentaje_iva_utilidad, 4),
            "total_aiu": round(total_aiu, 2),
            "porcentaje_total_aiu": round(porcentaje_total_aiu, 4),
            "valor_total_presupuesto": round(valor_total_presupuesto, 2)
        }

        self.repository.save_aiu(aiu_data)

        self.repository.update_budget_totals(
            presupuesto_id,
            {
                "total_administracion": aiu_data["total_administracion"],
                "total_imprevistos": aiu_data["total_imprevistos"],
                "total_utilidad": aiu_data["total_utilidad"],
                "iva_utilidad": aiu_data["iva_utilidad"],
                "valor_total_presupuesto": aiu_data["valor_total_presupuesto"]
            }
        )

        return aiu_data

    def to_float(self, value):
        try:
            if value is None or value == "":
                return 0
            return float(str(value).replace(",", "."))
        except Exception:
            return 0