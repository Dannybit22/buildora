from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class ManoObraRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="mano_obra",
            primary_key="id_mano_obra",
            fields=[
                "id_parametro",
                "codigo_mano_obra",
                "nombre_cargo",
                "cantidad_smmlv",
                "tipo_contratacion",
                "salario_base",
                "auxilio_transporte",
                "salud",
                "pension",
                "arl",
                "parafiscales",
                "prima",
                "cesantias",
                "intereses_cesantias",
                "total_contratacion",
                "porcentaje_prestacional",
                "dedicacion",
                "costo_dia",
                "dias_proyectados",
                "numero_trabajadores",
                "valor_total",
                "estado"
            ],
            search_fields=[
                "codigo_mano_obra",
                "nombre_cargo",
                "tipo_contratacion"
            ]
        )

    def get_all_with_params(self):
        query = """
            SELECT
                mo.id_mano_obra,
                mo.id_parametro,
                pg.nombre_version,
                mo.codigo_mano_obra,
                mo.nombre_cargo,
                mo.cantidad_smmlv,
                mo.tipo_contratacion,
                mo.salario_base,
                mo.total_contratacion,
                mo.porcentaje_prestacional,
                mo.dedicacion,
                mo.costo_dia,
                mo.dias_proyectados,
                mo.numero_trabajadores,
                mo.valor_total,
                mo.estado
            FROM mano_obra mo
            INNER JOIN parametros_generales pg 
                ON mo.id_parametro = pg.id_parametro
            WHERE mo.estado = 'activo'
            ORDER BY mo.id_mano_obra DESC;
        """
        return QueryExecutor.fetch_all(query)

    def search_with_params(self, text):
        query = """
            SELECT
                mo.id_mano_obra,
                mo.id_parametro,
                pg.nombre_version,
                mo.codigo_mano_obra,
                mo.nombre_cargo,
                mo.cantidad_smmlv,
                mo.tipo_contratacion,
                mo.salario_base,
                mo.total_contratacion,
                mo.porcentaje_prestacional,
                mo.dedicacion,
                mo.costo_dia,
                mo.dias_proyectados,
                mo.numero_trabajadores,
                mo.valor_total,
                mo.estado
            FROM mano_obra mo
            INNER JOIN parametros_generales pg 
                ON mo.id_parametro = pg.id_parametro
            WHERE mo.estado = 'activo'
            AND (
                mo.codigo_mano_obra LIKE %s
                OR mo.nombre_cargo LIKE %s
                OR mo.tipo_contratacion LIKE %s
            )
            ORDER BY mo.id_mano_obra DESC;
        """
        param = f"%{text}%"
        return QueryExecutor.fetch_all(query, (param, param, param))

    def get_by_id_with_params(self, mano_obra_id):
        query = """
            SELECT *
            FROM mano_obra
            WHERE id_mano_obra = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (mano_obra_id,))

    def get_current_params(self):
        query = """
            SELECT *
            FROM parametros_generales
            WHERE estado = 'activo'
            AND es_actual = 1
            ORDER BY id_parametro DESC
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query)