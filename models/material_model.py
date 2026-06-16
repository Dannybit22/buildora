class Material:
    def __init__(
        self,
        id_material=None,
        id_categoria_material=None,
        id_unidad=None,
        codigo_material="",
        descripcion="",
        valor_comercial_empaque=0,
        cantidad_por_empaque=1,
        precio_por_unidad=0,
        rendimiento=1,
        unidad_cotizacion="",
        valor_por_unidad_cotizacion=0,
        porcentaje_desperdicio=0,
        valor_desperdicio=0,
        valor_total=0,
        estado="activo"
    ):
        self.id_material = id_material
        self.id_categoria_material = id_categoria_material
        self.id_unidad = id_unidad
        self.codigo_material = codigo_material
        self.descripcion = descripcion
        self.valor_comercial_empaque = valor_comercial_empaque
        self.cantidad_por_empaque = cantidad_por_empaque
        self.precio_por_unidad = precio_por_unidad
        self.rendimiento = rendimiento
        self.unidad_cotizacion = unidad_cotizacion
        self.valor_por_unidad_cotizacion = valor_por_unidad_cotizacion
        self.porcentaje_desperdicio = porcentaje_desperdicio
        self.valor_desperdicio = valor_desperdicio
        self.valor_total = valor_total
        self.estado = estado