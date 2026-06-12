class Cliente:
    def __init__(
        self,
        id_cliente=None,
        tipo_cliente="Persona Natural",
        nombre_cliente="",
        identificacion="",
        telefono="",
        correo="",
        direccion="",
        ciudad="",
        observaciones="",
        estado="activo"
    ):
        self.id_cliente = id_cliente
        self.tipo_cliente = tipo_cliente
        self.nombre_cliente = nombre_cliente
        self.identificacion = identificacion
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.ciudad = ciudad
        self.observaciones = observaciones
        self.estado = estado