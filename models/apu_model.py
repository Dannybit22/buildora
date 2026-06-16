class Apu:
    def __init__(
        self,
        id_apu=None,
        id_unidad=None,
        codigo_apu="",
        descripcion="",
        cantidad_base=1,
        subtotal_materiales=0,
        subtotal_mano_obra=0,
        subtotal_herramientas=0,
        costo_directo_total=0,
        porcentaje_materiales=0,
        porcentaje_mano_obra=0,
        porcentaje_herramientas=0,
        observaciones="",
        estado="activo"
    ):
        self.id_apu = id_apu
        self.id_unidad = id_unidad
        self.codigo_apu = codigo_apu
        self.descripcion = descripcion
        self.cantidad_base = cantidad_base
        self.subtotal_materiales = subtotal_materiales
        self.subtotal_mano_obra = subtotal_mano_obra
        self.subtotal_herramientas = subtotal_herramientas
        self.costo_directo_total = costo_directo_total
        self.porcentaje_materiales = porcentaje_materiales
        self.porcentaje_mano_obra = porcentaje_mano_obra
        self.porcentaje_herramientas = porcentaje_herramientas
        self.observaciones = observaciones
        self.estado = estado