from database.query_executor import QueryExecutor
from repositories.base_repository import BaseRepository


class ApuRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="apus",
            primary_key="id_apu",
            fields=[
                "id_unidad",
                "codigo_apu",
                "descripcion",
                "cantidad_base",
                "subtotal_materiales",
                "subtotal_mano_obra",
                "subtotal_herramientas",
                "costo_directo_total",
                "porcentaje_materiales",
                "porcentaje_mano_obra",
                "porcentaje_herramientas",
                "observaciones",
                "estado"
            ],
            search_fields=[
                "codigo_apu",
                "descripcion"
            ]
        )

    def get_all_with_unit(self):
        query = """
            SELECT
                a.id_apu,
                a.id_unidad,
                u.codigo_unidad,
                a.codigo_apu,
                a.descripcion,
                a.cantidad_base,
                a.subtotal_materiales,
                a.subtotal_mano_obra,
                a.subtotal_herramientas,
                a.costo_directo_total,
                a.porcentaje_materiales,
                a.porcentaje_mano_obra,
                a.porcentaje_herramientas,
                a.observaciones,
                a.estado
            FROM apus a
            INNER JOIN unidades_medida u
                ON a.id_unidad = u.id_unidad
            WHERE a.estado = 'activo'
            ORDER BY a.id_apu DESC;
        """
        return QueryExecutor.fetch_all(query)

    def search_with_unit(self, text):
        query = """
            SELECT
                a.id_apu,
                a.id_unidad,
                u.codigo_unidad,
                a.codigo_apu,
                a.descripcion,
                a.cantidad_base,
                a.subtotal_materiales,
                a.subtotal_mano_obra,
                a.subtotal_herramientas,
                a.costo_directo_total,
                a.porcentaje_materiales,
                a.porcentaje_mano_obra,
                a.porcentaje_herramientas,
                a.observaciones,
                a.estado
            FROM apus a
            INNER JOIN unidades_medida u
                ON a.id_unidad = u.id_unidad
            WHERE a.estado = 'activo'
            AND (
                a.codigo_apu LIKE %s
                OR a.descripcion LIKE %s
                OR u.codigo_unidad LIKE %s
            )
            ORDER BY a.id_apu DESC;
        """
        param = f"%{text}%"
        return QueryExecutor.fetch_all(query, (param, param, param))

    def get_by_id_with_unit(self, apu_id):
        query = """
            SELECT
                a.*,
                u.codigo_unidad
            FROM apus a
            INNER JOIN unidades_medida u
                ON a.id_unidad = u.id_unidad
            WHERE a.id_apu = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (apu_id,))

    def get_active_units(self):
        query = """
            SELECT id_unidad, codigo_unidad, nombre_unidad
            FROM unidades_medida
            WHERE estado = 'activo'
            ORDER BY codigo_unidad ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_materials(self):
        query = """
            SELECT
                id_material,
                codigo_material,
                descripcion,
                unidad_cotizacion,
                valor_total
            FROM materiales
            WHERE estado = 'activo'
            ORDER BY descripcion ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_labor(self):
        query = """
            SELECT
                id_mano_obra,
                codigo_mano_obra,
                nombre_cargo,
                costo_dia
            FROM mano_obra
            WHERE estado = 'activo'
            ORDER BY nombre_cargo ASC;
        """
        return QueryExecutor.fetch_all(query)

    def get_active_tools(self):
        query = """
            SELECT
                id_herramienta,
                codigo_herramienta,
                nombre_herramienta,
                valor_por_obra
            FROM herramientas
            WHERE estado = 'activo'
            ORDER BY nombre_herramienta ASC;
        """
        return QueryExecutor.fetch_all(query)

    def add_material(self, data):
        query = """
            INSERT INTO apu_materiales (
                id_apu,
                id_material,
                descripcion_material,
                unidad_material,
                cantidad,
                valor_unitario,
                subtotal,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo');
        """
        return QueryExecutor.execute_return_id(
            query,
            (
                data["id_apu"],
                data["id_material"],
                data["descripcion_material"],
                data["unidad_material"],
                data["cantidad"],
                data["valor_unitario"],
                data["subtotal"]
            )
        )

    def add_labor(self, data):
        query = """
            INSERT INTO apu_mano_obra (
                id_apu,
                id_mano_obra,
                nombre_cargo,
                unidad_mano_obra,
                cantidad,
                valor_unitario,
                subtotal,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo');
        """
        return QueryExecutor.execute_return_id(
            query,
            (
                data["id_apu"],
                data["id_mano_obra"],
                data["nombre_cargo"],
                data["unidad_mano_obra"],
                data["cantidad"],
                data["valor_unitario"],
                data["subtotal"]
            )
        )

    def add_tool(self, data):
        query = """
            INSERT INTO apu_herramientas (
                id_apu,
                id_herramienta,
                nombre_herramienta,
                unidad_herramienta,
                cantidad,
                valor_unitario,
                subtotal,
                estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo');
        """
        return QueryExecutor.execute_return_id(
            query,
            (
                data["id_apu"],
                data["id_herramienta"],
                data["nombre_herramienta"],
                data["unidad_herramienta"],
                data["cantidad"],
                data["valor_unitario"],
                data["subtotal"]
            )
        )

    def get_apu_materials(self, apu_id):
        query = """
            SELECT *
            FROM apu_materiales
            WHERE id_apu = %s
            AND estado = 'activo'
            ORDER BY id_apu_material DESC;
        """
        return QueryExecutor.fetch_all(query, (apu_id,))

    def get_apu_labor(self, apu_id):
        query = """
            SELECT *
            FROM apu_mano_obra
            WHERE id_apu = %s
            AND estado = 'activo'
            ORDER BY id_apu_mano_obra DESC;
        """
        return QueryExecutor.fetch_all(query, (apu_id,))

    def get_apu_tools(self, apu_id):
        query = """
            SELECT *
            FROM apu_herramientas
            WHERE id_apu = %s
            AND estado = 'activo'
            ORDER BY id_apu_herramienta DESC;
        """
        return QueryExecutor.fetch_all(query, (apu_id,))

    def disable_material_detail(self, detail_id):
        query = """
            UPDATE apu_materiales
            SET estado = 'inactivo'
            WHERE id_apu_material = %s;
        """
        return QueryExecutor.execute(query, (detail_id,))

    def disable_labor_detail(self, detail_id):
        query = """
            UPDATE apu_mano_obra
            SET estado = 'inactivo'
            WHERE id_apu_mano_obra = %s;
        """
        return QueryExecutor.execute(query, (detail_id,))

    def disable_tool_detail(self, detail_id):
        query = """
            UPDATE apu_herramientas
            SET estado = 'inactivo'
            WHERE id_apu_herramienta = %s;
        """
        return QueryExecutor.execute(query, (detail_id,))

    def update_totals(self, apu_id, totals):
        query = """
            UPDATE apus
            SET
                subtotal_materiales = %s,
                subtotal_mano_obra = %s,
                subtotal_herramientas = %s,
                costo_directo_total = %s,
                porcentaje_materiales = %s,
                porcentaje_mano_obra = %s,
                porcentaje_herramientas = %s
            WHERE id_apu = %s;
        """
        return QueryExecutor.execute(
            query,
            (
                totals["subtotal_materiales"],
                totals["subtotal_mano_obra"],
                totals["subtotal_herramientas"],
                totals["costo_directo_total"],
                totals["porcentaje_materiales"],
                totals["porcentaje_mano_obra"],
                totals["porcentaje_herramientas"],
                apu_id
            )
        )