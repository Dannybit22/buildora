class Herramienta:

    def __init__(
        self,
        id_herramienta=None,
        id_categoria_herramienta=None,
        id_unidad=None,
        codigo_herramienta="",
        nombre_herramienta="",
        valor_comercial=0,
        rendimiento=1,
        numero_herramientas_obra=1,
        valor_hora=0,
        valor_por_obra=0,
        estado="activo"
    ):
        self.id_herramienta = id_herramienta
        self.id_categoria_herramienta = id_categoria_herramienta
        self.id_unidad = id_unidad
        self.codigo_herramienta = codigo_herramienta
        self.nombre_herramienta = nombre_herramienta
        self.valor_comercial = valor_comercial
        self.rendimiento = rendimiento
        self.numero_herramientas_obra = numero_herramientas_obra
        self.valor_hora = valor_hora
        self.valor_por_obra = valor_por_obra
        self.estado = estado