from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class PresupuestoRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="presupuestos",
            primary_key="id_presupuesto",
            fields=[
                "id_proyecto",
                "id_usuario_creador",
                "codigo_presupuesto",
                "nombre_presupuesto",
                "descripcion",
                "fecha_presupuesto",
                "costo_directo_total",
                "total_administracion",
                "total_imprevistos",
                "total_utilidad",
                "iva_utilidad",
                "valor_total_presupuesto",
                "estado",
                "observaciones"
            ],
            search_fields=[
                "codigo_presupuesto",
                "nombre_presupuesto",
                "descripcion"
            ]
        )

    def get_all_with_project(self):
        query = """
            SELECT
                pr.id_presupuesto,
                pr.id_proyecto,
                p.nombre_proyecto,
                c.nombre_cliente,
                pr.id_usuario_creador,
                pr.codigo_presupuesto,
                pr.nombre_presupuesto,
                pr.descripcion,
                pr.fecha_presupuesto,
                pr.costo_directo_total,
                pr.total_administracion,
                pr.total_imprevistos,
                pr.total_utilidad,
                pr.iva_utilidad,
                pr.valor_total_presupuesto,
                pr.estado,
                pr.observaciones
            FROM presupuestos pr
            INNER JOIN proyectos p
                ON pr.id_proyecto = p.id_proyecto
            INNER JOIN clientes c
                ON p.id_cliente = c.id_cliente
            WHERE pr.estado <> 'cerrado'
            ORDER BY pr.id_presupuesto DESC;
        """
        return QueryExecutor.fetch_all(query)

    def search_with_project(self, text):
        query = """
            SELECT
                pr.id_presupuesto,
                pr.id_proyecto,
                p.nombre_proyecto,
                c.nombre_cliente,
                pr.id_usuario_creador,
                pr.codigo_presupuesto,
                pr.nombre_presupuesto,
                pr.descripcion,
                pr.fecha_presupuesto,
                pr.costo_directo_total,
                pr.total_administracion,
                pr.total_imprevistos,
                pr.total_utilidad,
                pr.iva_utilidad,
                pr.valor_total_presupuesto,
                pr.estado,
                pr.observaciones
            FROM presupuestos pr
            INNER JOIN proyectos p
                ON pr.id_proyecto = p.id_proyecto
            INNER JOIN clientes c
                ON p.id_cliente = c.id_cliente
            WHERE pr.estado <> 'cerrado'
            AND (
                pr.codigo_presupuesto LIKE %s
                OR pr.nombre_presupuesto LIKE %s
                OR p.nombre_proyecto LIKE %s
                OR c.nombre_cliente LIKE %s
            )
            ORDER BY pr.id_presupuesto DESC;
        """
        param = f"%{text}%"
        return QueryExecutor.fetch_all(query, (param, param, param, param))

    def get_by_id_with_project(self, presupuesto_id):
        query = """
            SELECT
                pr.*,
                p.nombre_proyecto,
                c.nombre_cliente
            FROM presupuestos pr
            INNER JOIN proyectos p
                ON pr.id_proyecto = p.id_proyecto
            INNER JOIN clientes c
                ON p.id_cliente = c.id_cliente
            WHERE pr.id_presupuesto = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (presupuesto_id,))

    def get_active_projects_without_budget(self):
        query = """
            SELECT
                p.id_proyecto,
                p.codigo_proyecto,
                p.nombre_proyecto,
                c.nombre_cliente
            FROM proyectos p
            INNER JOIN clientes c
                ON p.id_cliente = c.id_cliente
            LEFT JOIN presupuestos pr
                ON p.id_proyecto = pr.id_proyecto
                AND pr.estado <> 'cerrado'
            WHERE p.estado = 'activo'
            AND pr.id_presupuesto IS NULL
            ORDER BY p.nombre_proyecto ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_projects(self):
        query = """
            SELECT
                p.id_proyecto,
                p.codigo_proyecto,
                p.nombre_proyecto,
                c.nombre_cliente
            FROM proyectos p
            INNER JOIN clientes c
                ON p.id_cliente = c.id_cliente
            WHERE p.estado = 'activo'
            ORDER BY p.nombre_proyecto ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_apus(self):
        query = """
            SELECT
                a.id_apu,
                a.codigo_apu,
                a.descripcion,
                u.codigo_unidad,
                a.costo_directo_total,
                a.subtotal_materiales,
                a.subtotal_mano_obra,
                a.subtotal_herramientas
            FROM apus a
            INNER JOIN unidades_medida u
                ON a.id_unidad = u.id_unidad
            WHERE a.estado = 'activo'
            ORDER BY a.descripcion ASC;
        """
        return QueryExecutor.fetch_all(query)

    def close_budget(self, presupuesto_id):
        query = """
            UPDATE presupuestos
            SET estado = 'cerrado'
            WHERE id_presupuesto = %s;
        """
        return QueryExecutor.execute(query, (presupuesto_id,))


class PresupuestoCapituloRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="presupuesto_capitulos",
            primary_key="id_capitulo",
            fields=[
                "id_presupuesto",
                "codigo_capitulo",
                "nombre_capitulo",
                "descripcion",
                "orden",
                "costo_total_capitulo",
                "porcentaje_participacion",
                "estado"
            ],
            search_fields=[
                "codigo_capitulo",
                "nombre_capitulo"
            ]
        )

    def get_by_budget(self, presupuesto_id):
        query = """
            SELECT *
            FROM presupuesto_capitulos
            WHERE id_presupuesto = %s
            AND estado = 'activo'
            ORDER BY orden ASC, id_capitulo ASC;
        """
        return QueryExecutor.fetch_all(query, (presupuesto_id,))

    def update_total(self, capitulo_id, total):
        query = """
            UPDATE presupuesto_capitulos
            SET costo_total_capitulo = %s
            WHERE id_capitulo = %s;
        """
        return QueryExecutor.execute(query, (total, capitulo_id))

    def update_percentage(self, capitulo_id, porcentaje):
        query = """
            UPDATE presupuesto_capitulos
            SET porcentaje_participacion = %s
            WHERE id_capitulo = %s;
        """
        return QueryExecutor.execute(query, (porcentaje, capitulo_id))


class PresupuestoItemRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="presupuesto_items",
            primary_key="id_item",
            fields=[
                "id_capitulo",
                "id_apu",
                "codigo_item",
                "descripcion_item",
                "unidad_item",
                "cantidad",
                "costo_unitario_historico",
                "costo_total_item",
                "codigo_apu_historico",
                "descripcion_apu_historica",
                "unidad_apu_historica",
                "subtotal_materiales_historico",
                "subtotal_mano_obra_historico",
                "subtotal_herramientas_historico",
                "orden",
                "estado"
            ],
            search_fields=[
                "codigo_item",
                "descripcion_item"
            ]
        )

    def get_by_chapter(self, capitulo_id):
        query = """
            SELECT *
            FROM presupuesto_items
            WHERE id_capitulo = %s
            AND estado = 'activo'
            ORDER BY orden ASC, id_item ASC;
        """
        return QueryExecutor.fetch_all(query, (capitulo_id,))

    def get_by_budget(self, presupuesto_id):
        query = """
            SELECT
                i.*,
                c.codigo_capitulo,
                c.nombre_capitulo
            FROM presupuesto_items i
            INNER JOIN presupuesto_capitulos c
                ON i.id_capitulo = c.id_capitulo
            WHERE c.id_presupuesto = %s
            AND i.estado = 'activo'
            AND c.estado = 'activo'
            ORDER BY c.orden ASC, i.orden ASC;
        """
        return QueryExecutor.fetch_all(query, (presupuesto_id,))

    def get_apu_snapshot(self, apu_id):
        query = """
            SELECT
                a.id_apu,
                a.codigo_apu,
                a.descripcion,
                u.codigo_unidad,
                a.costo_directo_total,
                a.subtotal_materiales,
                a.subtotal_mano_obra,
                a.subtotal_herramientas
            FROM apus a
            INNER JOIN unidades_medida u
                ON a.id_unidad = u.id_unidad
            WHERE a.id_apu = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (apu_id,))

    def sum_chapter_items(self, capitulo_id):
        query = """
            SELECT COALESCE(SUM(costo_total_item), 0) AS total
            FROM presupuesto_items
            WHERE id_capitulo = %s
            AND estado = 'activo';
        """
        result = QueryExecutor.fetch_one(query, (capitulo_id,))
        return float(result["total"] or 0)

    def sum_budget_items(self, presupuesto_id):
        query = """
            SELECT COALESCE(SUM(i.costo_total_item), 0) AS total
            FROM presupuesto_items i
            INNER JOIN presupuesto_capitulos c
                ON i.id_capitulo = c.id_capitulo
            WHERE c.id_presupuesto = %s
            AND i.estado = 'activo'
            AND c.estado = 'activo';
        """
        result = QueryExecutor.fetch_one(query, (presupuesto_id,))
        return float(result["total"] or 0)