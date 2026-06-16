from database.query_executor import QueryExecutor


class DashboardRepository:

    def count_table(self, table_name):
        query = f"""
            SELECT COUNT(*) AS total
            FROM {table_name}
            WHERE estado = 'activo';
        """

        result = QueryExecutor.fetch_one(query)

        if not result:
            return 0

        return result["total"] or 0

    def count_presupuestos(self):
        query = """
            SELECT COUNT(*) AS total
            FROM presupuestos
            WHERE estado <> 'cerrado';
        """

        result = QueryExecutor.fetch_one(query)

        if not result:
            return 0

        return result["total"] or 0

    def total_valor_presupuestado(self):
        query = """
            SELECT COALESCE(SUM(valor_total_presupuesto), 0) AS total
            FROM presupuestos
            WHERE estado <> 'cerrado';
        """

        result = QueryExecutor.fetch_one(query)

        if not result:
            return 0

        return result["total"] or 0

    def total_costo_directo(self):
        query = """
            SELECT COALESCE(SUM(costo_directo_total), 0) AS total
            FROM presupuestos
            WHERE estado <> 'cerrado';
        """

        result = QueryExecutor.fetch_one(query)

        if not result:
            return 0

        return result["total"] or 0

    def get_latest_budgets(self):
        query = """
            SELECT
                pr.codigo_presupuesto,
                pr.nombre_presupuesto,
                p.nombre_proyecto,
                pr.valor_total_presupuesto,
                pr.estado
            FROM presupuestos pr
            INNER JOIN proyectos p
                ON pr.id_proyecto = p.id_proyecto
            WHERE pr.estado <> 'cerrado'
            ORDER BY pr.id_presupuesto DESC
            LIMIT 5;
        """

        return QueryExecutor.fetch_all(query)