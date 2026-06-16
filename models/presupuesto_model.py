class Presupuesto:
    def __init__(
        self,
        id_presupuesto=None,
        id_proyecto=None,
        id_usuario_creador=None,
        codigo_presupuesto="",
        nombre_presupuesto="",
        descripcion="",
        fecha_presupuesto="",
        costo_directo_total=0,
        total_administracion=0,
        total_imprevistos=0,
        total_utilidad=0,
        iva_utilidad=0,
        valor_total_presupuesto=0,
        estado="borrador",
        observaciones=""
    ):
        self.id_presupuesto = id_presupuesto
        self.id_proyecto = id_proyecto
        self.id_usuario_creador = id_usuario_creador
        self.codigo_presupuesto = codigo_presupuesto
        self.nombre_presupuesto = nombre_presupuesto
        self.descripcion = descripcion
        self.fecha_presupuesto = fecha_presupuesto
        self.costo_directo_total = costo_directo_total
        self.total_administracion = total_administracion
        self.total_imprevistos = total_imprevistos
        self.total_utilidad = total_utilidad
        self.iva_utilidad = iva_utilidad
        self.valor_total_presupuesto = valor_total_presupuesto
        self.estado = estado
        self.observaciones = observaciones


class PresupuestoCapitulo:
    def __init__(
        self,
        id_capitulo=None,
        id_presupuesto=None,
        codigo_capitulo="",
        nombre_capitulo="",
        descripcion="",
        orden=1,
        costo_total_capitulo=0,
        porcentaje_participacion=0,
        estado="activo"
    ):
        self.id_capitulo = id_capitulo
        self.id_presupuesto = id_presupuesto
        self.codigo_capitulo = codigo_capitulo
        self.nombre_capitulo = nombre_capitulo
        self.descripcion = descripcion
        self.orden = orden
        self.costo_total_capitulo = costo_total_capitulo
        self.porcentaje_participacion = porcentaje_participacion
        self.estado = estado


class PresupuestoItem:
    def __init__(
        self,
        id_item=None,
        id_capitulo=None,
        id_apu=None,
        codigo_item="",
        descripcion_item="",
        unidad_item="",
        cantidad=1,
        costo_unitario_historico=0,
        costo_total_item=0,
        codigo_apu_historico="",
        descripcion_apu_historica="",
        unidad_apu_historica="",
        subtotal_materiales_historico=0,
        subtotal_mano_obra_historico=0,
        subtotal_herramientas_historico=0,
        orden=1,
        estado="activo"
    ):
        self.id_item = id_item
        self.id_capitulo = id_capitulo
        self.id_apu = id_apu
        self.codigo_item = codigo_item
        self.descripcion_item = descripcion_item
        self.unidad_item = unidad_item
        self.cantidad = cantidad
        self.costo_unitario_historico = costo_unitario_historico
        self.costo_total_item = costo_total_item
        self.codigo_apu_historico = codigo_apu_historico
        self.descripcion_apu_historica = descripcion_apu_historica
        self.unidad_apu_historica = unidad_apu_historica
        self.subtotal_materiales_historico = subtotal_materiales_historico
        self.subtotal_mano_obra_historico = subtotal_mano_obra_historico
        self.subtotal_herramientas_historico = subtotal_herramientas_historico
        self.orden = orden
        self.estado = estado