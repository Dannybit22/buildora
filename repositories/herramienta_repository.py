from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class HerramientaRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="herramientas",
            primary_key="id_herramienta",
            fields=[
                "id_categoria_herramienta",
                "id_unidad",
                "codigo_herramienta",
                "nombre_herramienta",
                "valor_comercial",
                "rendimiento",
                "numero_herramientas_obra",
                "valor_hora",
                "valor_por_obra",
                "estado"
            ],
            search_fields=[
                "codigo_herramienta",
                "nombre_herramienta"
            ]
        )

    def get_all_with_relations(self):

        query = """
            SELECT
                h.id_herramienta,
                h.id_categoria_herramienta,
                ch.nombre_categoria,
                h.id_unidad,
                um.codigo_unidad,
                h.codigo_herramienta,
                h.nombre_herramienta,
                h.valor_comercial,
                h.rendimiento,
                h.numero_herramientas_obra,
                h.valor_hora,
                h.valor_por_obra,
                h.estado
            FROM herramientas h
            INNER JOIN categorias_herramientas ch
                ON h.id_categoria_herramienta = ch.id_categoria_herramienta
            INNER JOIN unidades_medida um
                ON h.id_unidad = um.id_unidad
            WHERE h.estado = 'activo'
            ORDER BY h.id_herramienta DESC
        """

        return QueryExecutor.fetch_all(query)

    def search_with_relations(self, text):

        query = """
            SELECT
                h.id_herramienta,
                h.id_categoria_herramienta,
                ch.nombre_categoria,
                h.id_unidad,
                um.codigo_unidad,
                h.codigo_herramienta,
                h.nombre_herramienta,
                h.valor_comercial,
                h.rendimiento,
                h.numero_herramientas_obra,
                h.valor_hora,
                h.valor_por_obra,
                h.estado
            FROM herramientas h
            INNER JOIN categorias_herramientas ch
                ON h.id_categoria_herramienta = ch.id_categoria_herramienta
            INNER JOIN unidades_medida um
                ON h.id_unidad = um.id_unidad
            WHERE h.estado='activo'
            AND (
                h.codigo_herramienta LIKE %s
                OR h.nombre_herramienta LIKE %s
                OR ch.nombre_categoria LIKE %s
                OR um.codigo_unidad LIKE %s
            )
            ORDER BY h.id_herramienta DESC
        """

        param = f"%{text}%"

        return QueryExecutor.fetch_all(
            query,
            (param, param, param, param)
        )

    def get_by_id_with_relations(self, herramienta_id):

        query = """
            SELECT
                h.id_herramienta,
                h.id_categoria_herramienta,
                h.id_unidad,
                h.codigo_herramienta,
                h.nombre_herramienta,
                h.valor_comercial,
                h.rendimiento,
                h.numero_herramientas_obra,
                h.valor_hora,
                h.valor_por_obra,
                h.estado
            FROM herramientas h
            WHERE h.id_herramienta=%s
            LIMIT 1
        """

        return QueryExecutor.fetch_one(
            query,
            (herramienta_id,)
        )

    def get_active_categories(self):

        query = """
            SELECT
                id_categoria_herramienta,
                nombre_categoria
            FROM categorias_herramientas
            WHERE estado='activo'
            ORDER BY nombre_categoria
        """

        return QueryExecutor.fetch_all(query)

    def get_active_units(self):

        query = """
            SELECT
                id_unidad,
                codigo_unidad,
                nombre_unidad
            FROM unidades_medida
            WHERE estado='activo'
            ORDER BY codigo_unidad
        """

        return QueryExecutor.fetch_all(query)