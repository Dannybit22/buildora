from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class MaterialRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="materiales",
            primary_key="id_material",
            fields=[
                "id_categoria_material",
                "id_unidad",
                "codigo_material",
                "descripcion",
                "valor_comercial_empaque",
                "cantidad_por_empaque",
                "precio_por_unidad",
                "rendimiento",
                "unidad_cotizacion",
                "valor_por_unidad_cotizacion",
                "porcentaje_desperdicio",
                "valor_desperdicio",
                "valor_total",
                "estado"
            ],
            search_fields=[
                "codigo_material",
                "descripcion",
                "unidad_cotizacion"
            ]
        )

    def get_all_with_relations(self):
        query = """
            SELECT
                m.id_material,
                m.id_categoria_material,
                cm.nombre_categoria,
                m.id_unidad,
                u.codigo_unidad,
                m.codigo_material,
                m.descripcion,
                m.valor_comercial_empaque,
                m.cantidad_por_empaque,
                m.precio_por_unidad,
                m.rendimiento,
                m.unidad_cotizacion,
                m.valor_por_unidad_cotizacion,
                m.porcentaje_desperdicio,
                m.valor_desperdicio,
                m.valor_total,
                m.estado
            FROM materiales m
            LEFT JOIN categorias_materiales cm
                ON m.id_categoria_material = cm.id_categoria_material
            INNER JOIN unidades_medida u
                ON m.id_unidad = u.id_unidad
            WHERE m.estado = 'activo'
            ORDER BY m.id_material DESC;
        """
        return QueryExecutor.fetch_all(query)

    def search_with_relations(self, text):
        query = """
            SELECT
                m.id_material,
                m.id_categoria_material,
                cm.nombre_categoria,
                m.id_unidad,
                u.codigo_unidad,
                m.codigo_material,
                m.descripcion,
                m.valor_comercial_empaque,
                m.cantidad_por_empaque,
                m.precio_por_unidad,
                m.rendimiento,
                m.unidad_cotizacion,
                m.valor_por_unidad_cotizacion,
                m.porcentaje_desperdicio,
                m.valor_desperdicio,
                m.valor_total,
                m.estado
            FROM materiales m
            LEFT JOIN categorias_materiales cm
                ON m.id_categoria_material = cm.id_categoria_material
            INNER JOIN unidades_medida u
                ON m.id_unidad = u.id_unidad
            WHERE m.estado = 'activo'
            AND (
                m.codigo_material LIKE %s
                OR m.descripcion LIKE %s
                OR cm.nombre_categoria LIKE %s
                OR u.codigo_unidad LIKE %s
            )
            ORDER BY m.id_material DESC;
        """
        param = f"%{text}%"
        return QueryExecutor.fetch_all(query, (param, param, param, param))

    def get_by_id_with_relations(self, material_id):
        query = """
            SELECT
                m.id_material,
                m.id_categoria_material,
                cm.nombre_categoria,
                m.id_unidad,
                u.codigo_unidad,
                m.codigo_material,
                m.descripcion,
                m.valor_comercial_empaque,
                m.cantidad_por_empaque,
                m.precio_por_unidad,
                m.rendimiento,
                m.unidad_cotizacion,
                m.valor_por_unidad_cotizacion,
                m.porcentaje_desperdicio,
                m.valor_desperdicio,
                m.valor_total,
                m.estado
            FROM materiales m
            LEFT JOIN categorias_materiales cm
                ON m.id_categoria_material = cm.id_categoria_material
            INNER JOIN unidades_medida u
                ON m.id_unidad = u.id_unidad
            WHERE m.id_material = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (material_id,))

    def get_active_categories(self):
        query = """
            SELECT id_categoria_material, nombre_categoria
            FROM categorias_materiales
            WHERE estado = 'activo'
            ORDER BY nombre_categoria ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_units(self):
        query = """
            SELECT id_unidad, codigo_unidad, nombre_unidad
            FROM unidades_medida
            WHERE estado = 'activo'
            ORDER BY id_unidad ASC;
        """
        return QueryExecutor.fetch_all(query)