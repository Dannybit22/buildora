class Proyecto:
    def __init__(
        self,
        id_proyecto=None,
        id_cliente=None,
        codigo_proyecto="",
        nombre_proyecto="",
        ubicacion="",
        fecha_proyecto="",
        descripcion="",
        observaciones="",
        estado="activo"
    ):
        self.id_proyecto = id_proyecto
        self.id_cliente = id_cliente
        self.codigo_proyecto = codigo_proyecto
        self.nombre_proyecto = nombre_proyecto
        self.ubicacion = ubicacion
        self.fecha_proyecto = fecha_proyecto
        self.descripcion = descripcion
        self.observaciones = observaciones
        self.estado = estado