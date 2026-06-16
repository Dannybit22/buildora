from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class ProyectoRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="proyectos",
            primary_key="id_proyecto",
            fields=[
                "id_cliente",
                "codigo_proyecto",
                "nombre_proyecto",
                "ubicacion",
                "fecha_proyecto",
                "descripcion",
                "observaciones",
                "estado"
            ],
            search_fields=[
                "codigo_proyecto",
                "nombre_proyecto",
                "ubicacion"
            ]
        )

    def get_all_with_client(self):
        query = """
            SELECT
                p.id_proyecto,
                p.id_cliente,
                c.nombre_cliente,
                p.codigo_proyecto,
                p.nombre_proyecto,
                p.ubicacion,
                p.fecha_proyecto,
                p.descripcion,
                p.observaciones,
                p.estado
            FROM proyectos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.estado = 'activo'
            ORDER BY p.id_proyecto DESC;
        """

        return QueryExecutor.fetch_all(query)

    def search_with_client(self, text):
        query = """
            SELECT
                p.id_proyecto,
                p.id_cliente,
                c.nombre_cliente,
                p.codigo_proyecto,
                p.nombre_proyecto,
                p.ubicacion,
                p.fecha_proyecto,
                p.descripcion,
                p.observaciones,
                p.estado
            FROM proyectos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.estado = 'activo'
            AND (
                p.codigo_proyecto LIKE %s
                OR p.nombre_proyecto LIKE %s
                OR p.ubicacion LIKE %s
                OR c.nombre_cliente LIKE %s
            )
            ORDER BY p.id_proyecto DESC;
        """

        param = f"%{text}%"
        return QueryExecutor.fetch_all(query, (param, param, param, param))

    def get_by_id_with_client(self, proyecto_id):
        query = """
            SELECT
                p.id_proyecto,
                p.id_cliente,
                c.nombre_cliente,
                p.codigo_proyecto,
                p.nombre_proyecto,
                p.ubicacion,
                p.fecha_proyecto,
                p.descripcion,
                p.observaciones,
                p.estado
            FROM proyectos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE p.id_proyecto = %s
            LIMIT 1;
        """

        return QueryExecutor.fetch_one(query, (proyecto_id,))

    def get_active_clients(self):
        query = """
            SELECT
                id_cliente,
                nombre_cliente
            FROM clientes
            WHERE estado = 'activo'
            ORDER BY nombre_cliente ASC;
        """

        return QueryExecutor.fetch_all(query)