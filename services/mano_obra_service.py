from repositories.mano_obra_repository import ManoObraRepository


class ManoObraService:

    def __init__(self):
        self.repository = ManoObraRepository()

    def get_all(self):
        return self.repository.get_all_with_params()

    def search(self, text):
        if not text:
            return self.get_all()
        return self.repository.search_with_params(text)

    def get_by_id(self, mano_obra_id):
        return self.repository.get_by_id_with_params(mano_obra_id)

    def create(self, data):
        data = self.prepare_data(data)
        self.validate(data)
        return self.repository.create(data)

    def update(self, mano_obra_id, data):
        data = self.prepare_data(data)
        self.validate(data)
        return self.repository.update(mano_obra_id, data)

    def disable(self, mano_obra_id):
        return self.repository.disable(mano_obra_id)

    def prepare_data(self, data):
        params = self.repository.get_current_params()

        if not params:
            raise ValueError("No existen parámetros generales activos.")

        cantidad_smmlv = self.to_float(data.get("cantidad_smmlv"))
        dedicacion = self.to_float(data.get("dedicacion"))

        if dedicacion > 1:
            dedicacion = dedicacion / 100
        dias_proyectados = self.to_float(data.get("dias_proyectados"))
        numero_trabajadores = self.to_float(data.get("numero_trabajadores"))

        if cantidad_smmlv <= 0:
            cantidad_smmlv = 1

        if dedicacion <= 0:
            dedicacion = 1

        if numero_trabajadores <= 0:
            numero_trabajadores = 1

        tipo_contratacion = data.get("tipo_contratacion")

        salario_base = cantidad_smmlv * float(params["smmlv"])

        auxilio_transporte = 0
        salud = 0
        pension = 0
        arl = 0
        parafiscales = 0
        prima = 0
        cesantias = 0
        intereses_cesantias = 0

        if tipo_contratacion == "contrato_completo":
            auxilio_transporte = float(params["auxilio_transporte"])
            salud = salario_base * float(params["porcentaje_salud"])
            pension = salario_base * float(params["porcentaje_pension"])
            arl = salario_base * float(params["porcentaje_arl"])
            parafiscales = salario_base * float(params["porcentaje_parafiscales"])
            prima = salario_base * float(params["porcentaje_prima"])
            cesantias = salario_base * float(params["porcentaje_cesantias"])
            intereses_cesantias = cesantias * float(params["porcentaje_intereses_cesantias"])

        total_prestaciones = (
            auxilio_transporte
            + salud
            + pension
            + arl
            + parafiscales
            + prima
            + cesantias
            + intereses_cesantias
        )

        total_contratacion = salario_base + total_prestaciones

        porcentaje_prestacional = 0
        if salario_base > 0:
            porcentaje_prestacional = (total_prestaciones / salario_base) * 100

        costo_dia = (total_contratacion / 30) * dedicacion

        valor_total = costo_dia * dias_proyectados * numero_trabajadores

        return {
            "id_parametro": params["id_parametro"],
            "codigo_mano_obra": data.get("codigo_mano_obra", "").strip(),
            "nombre_cargo": data.get("nombre_cargo", "").strip(),
            "cantidad_smmlv": cantidad_smmlv,
            "tipo_contratacion": tipo_contratacion,
            "salario_base": round(salario_base, 2),
            "auxilio_transporte": round(auxilio_transporte, 2),
            "salud": round(salud, 2),
            "pension": round(pension, 2),
            "arl": round(arl, 2),
            "parafiscales": round(parafiscales, 2),
            "prima": round(prima, 2),
            "cesantias": round(cesantias, 2),
            "intereses_cesantias": round(intereses_cesantias, 2),
            "total_contratacion": round(total_contratacion, 2),
            "porcentaje_prestacional": round(porcentaje_prestacional, 4),
            "dedicacion": dedicacion,
            "costo_dia": round(costo_dia, 2),
            "dias_proyectados": dias_proyectados,
            "numero_trabajadores": numero_trabajadores,
            "valor_total": round(valor_total, 2),
            "estado": "activo"
        }

    def validate(self, data):
        if not data.get("codigo_mano_obra"):
            raise ValueError("El código de mano de obra es obligatorio.")

        if not data.get("nombre_cargo"):
            raise ValueError("El nombre del cargo es obligatorio.")

        if data.get("cantidad_smmlv", 0) <= 0:
            raise ValueError("La cantidad de SMMLV debe ser mayor que cero.")

        if data.get("dedicacion", 0) <= 0:
            raise ValueError("La dedicación debe ser mayor que cero.")

        if data.get("dias_proyectados", 0) < 0:
            raise ValueError("Los días proyectados no pueden ser negativos.")

        if data.get("numero_trabajadores", 0) <= 0:
            raise ValueError("El número de trabajadores debe ser mayor que cero.")

    def to_float(self, value):
        try:
            if value is None or value == "":
                return 0
            return float(str(value).replace(",", "."))
        except Exception:
            return 0