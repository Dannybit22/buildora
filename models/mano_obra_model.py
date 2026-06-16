class ManoObra:
    def __init__(
        self,
        id_mano_obra=None,
        id_parametro=None,
        codigo_mano_obra="",
        nombre_cargo="",
        cantidad_smmlv=1,
        tipo_contratacion="contrato_completo",
        dedicacion=1,
        dias_proyectados=0,
        numero_trabajadores=1,
        estado="activo"
    ):
        self.id_mano_obra = id_mano_obra
        self.id_parametro = id_parametro
        self.codigo_mano_obra = codigo_mano_obra
        self.nombre_cargo = nombre_cargo
        self.cantidad_smmlv = cantidad_smmlv
        self.tipo_contratacion = tipo_contratacion
        self.dedicacion = dedicacion
        self.dias_proyectados = dias_proyectados
        self.numero_trabajadores = numero_trabajadores
        self.estado = estado