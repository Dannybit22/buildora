from database.query_executor import QueryExecutor


class AiuRepository:

    def get_budget(self, presupuesto_id):
        query = """
            SELECT *
            FROM presupuestos
            WHERE id_presupuesto = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (presupuesto_id,))

    def get_active_budgets(self):
        query = """
            SELECT
                pr.id_presupuesto,
                pr.codigo_presupuesto,
                pr.nombre_presupuesto,
                p.nombre_proyecto,
                pr.costo_directo_total,
                pr.total_administracion,
                pr.total_imprevistos,
                pr.total_utilidad,
                pr.iva_utilidad,
                pr.valor_total_presupuesto
            FROM presupuestos pr
            INNER JOIN proyectos p
                ON pr.id_proyecto = p.id_proyecto
            WHERE pr.estado <> 'cerrado'
            ORDER BY pr.id_presupuesto DESC;
        """
        return QueryExecutor.fetch_all(query)

    def get_administracion(self, presupuesto_id):
        query = """
            SELECT *
            FROM administracion_presupuesto
            WHERE id_presupuesto = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (presupuesto_id,))

    def save_administracion(self, data):
        existing = self.get_administracion(data["id_presupuesto"])

        if existing:
            query = """
                UPDATE administracion_presupuesto
                SET
                    total_personal_tecnico = %s,
                    total_personal_administrativo = %s,
                    total_ocupacional = %s,
                    total_dotacion_oficina = %s,
                    total_equipos = %s,
                    total_caja_menor = %s,
                    total_garantias = %s,
                    total_impuestos = %s,
                    total_administracion = %s,
                    porcentaje_administracion = %s,
                    observaciones = %s
                WHERE id_presupuesto = %s;
            """
            params = (
                data["total_personal_tecnico"],
                data["total_personal_administrativo"],
                data["total_ocupacional"],
                data["total_dotacion_oficina"],
                data["total_equipos"],
                data["total_caja_menor"],
                data["total_garantias"],
                data["total_impuestos"],
                data["total_administracion"],
                data["porcentaje_administracion"],
                data["observaciones"],
                data["id_presupuesto"]
            )
            return QueryExecutor.execute(query, params)

        query = """
            INSERT INTO administracion_presupuesto (
                id_presupuesto,
                total_personal_tecnico,
                total_personal_administrativo,
                total_ocupacional,
                total_dotacion_oficina,
                total_equipos,
                total_caja_menor,
                total_garantias,
                total_impuestos,
                total_administracion,
                porcentaje_administracion,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            data["id_presupuesto"],
            data["total_personal_tecnico"],
            data["total_personal_administrativo"],
            data["total_ocupacional"],
            data["total_dotacion_oficina"],
            data["total_equipos"],
            data["total_caja_menor"],
            data["total_garantias"],
            data["total_impuestos"],
            data["total_administracion"],
            data["porcentaje_administracion"],
            data["observaciones"]
        )
        return QueryExecutor.execute_return_id(query, params)

    def get_imprevistos(self, presupuesto_id):
        query = """
            SELECT *
            FROM imprevistos_presupuesto
            WHERE id_presupuesto = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (presupuesto_id,))

    def save_imprevistos(self, data):
        existing = self.get_imprevistos(data["id_presupuesto"])

        if existing:
            query = """
                UPDATE imprevistos_presupuesto
                SET
                    total_imprevisto_mano_obra = %s,
                    total_imprevisto_materiales = %s,
                    total_imprevisto_riesgo = %s,
                    total_imprevisto_administracion = %s,
                    total_imprevistos = %s,
                    porcentaje_imprevistos = %s,
                    observaciones = %s
                WHERE id_presupuesto = %s;
            """
            params = (
                data["total_imprevisto_mano_obra"],
                data["total_imprevisto_materiales"],
                data["total_imprevisto_riesgo"],
                data["total_imprevisto_administracion"],
                data["total_imprevistos"],
                data["porcentaje_imprevistos"],
                data["observaciones"],
                data["id_presupuesto"]
            )
            return QueryExecutor.execute(query, params)

        query = """
            INSERT INTO imprevistos_presupuesto (
                id_presupuesto,
                total_imprevisto_mano_obra,
                total_imprevisto_materiales,
                total_imprevisto_riesgo,
                total_imprevisto_administracion,
                total_imprevistos,
                porcentaje_imprevistos,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            data["id_presupuesto"],
            data["total_imprevisto_mano_obra"],
            data["total_imprevisto_materiales"],
            data["total_imprevisto_riesgo"],
            data["total_imprevisto_administracion"],
            data["total_imprevistos"],
            data["porcentaje_imprevistos"],
            data["observaciones"]
        )
        return QueryExecutor.execute_return_id(query, params)

    def get_utilidad(self, presupuesto_id):
        query = """
            SELECT *
            FROM utilidad_presupuesto
            WHERE id_presupuesto = %s
            LIMIT 1;
        """
        return QueryExecutor.fetch_one(query, (presupuesto_id,))

    def save_utilidad(self, data):
        existing = self.get_utilidad(data["id_presupuesto"])

        if existing:
            query = """
                UPDATE utilidad_presupuesto
                SET
                    porcentaje_utilidad_operativa = %s,
                    utilidad_operativa = %s,
                    porcentaje_retefuente = %s,
                    valor_retefuente = %s,
                    porcentaje_renta = %s,
                    valor_renta = %s,
                    total_utilidad = %s,
                    porcentaje_iva_utilidad = %s,
                    iva_utilidad = %s,
                    observaciones = %s
                WHERE id_presupuesto = %s;
            """
            params = (
                data["porcentaje_utilidad_operativa"],
                data["utilidad_operativa"],
                data["porcentaje_retefuente"],
                data["valor_retefuente"],
                data["porcentaje_renta"],
                data["valor_renta"],
                data["total_utilidad"],
                data["porcentaje_iva_utilidad"],
                data["iva_utilidad"],
                data["observaciones"],
                data["id_presupuesto"]
            )
            return QueryExecutor.execute(query, params)

        query = """
            INSERT INTO utilidad_presupuesto (
                id_presupuesto,
                porcentaje_utilidad_operativa,
                utilidad_operativa,
                porcentaje_retefuente,
                valor_retefuente,
                porcentaje_renta,
                valor_renta,
                total_utilidad,
                porcentaje_iva_utilidad,
                iva_utilidad,
                observaciones
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            data["id_presupuesto"],
            data["porcentaje_utilidad_operativa"],
            data["utilidad_operativa"],
            data["porcentaje_retefuente"],
            data["valor_retefuente"],
            data["porcentaje_renta"],
            data["valor_renta"],
            data["total_utilidad"],
            data["porcentaje_iva_utilidad"],
            data["iva_utilidad"],
            data["observaciones"]
        )
        return QueryExecutor.execute_return_id(query, params)

    def save_aiu(self, data):
        existing = QueryExecutor.fetch_one(
            "SELECT * FROM aiu_presupuesto WHERE id_presupuesto = %s LIMIT 1;",
            (data["id_presupuesto"],)
        )

        if existing:
            query = """
                UPDATE aiu_presupuesto
                SET
                    costo_directo_total = %s,
                    total_administracion = %s,
                    porcentaje_administracion = %s,
                    total_imprevistos = %s,
                    porcentaje_imprevistos = %s,
                    total_utilidad = %s,
                    porcentaje_utilidad = %s,
                    iva_utilidad = %s,
                    porcentaje_iva_utilidad = %s,
                    total_aiu = %s,
                    porcentaje_total_aiu = %s,
                    valor_total_presupuesto = %s
                WHERE id_presupuesto = %s;
            """
            params = (
                data["costo_directo_total"],
                data["total_administracion"],
                data["porcentaje_administracion"],
                data["total_imprevistos"],
                data["porcentaje_imprevistos"],
                data["total_utilidad"],
                data["porcentaje_utilidad"],
                data["iva_utilidad"],
                data["porcentaje_iva_utilidad"],
                data["total_aiu"],
                data["porcentaje_total_aiu"],
                data["valor_total_presupuesto"],
                data["id_presupuesto"]
            )
            return QueryExecutor.execute(query, params)

        query = """
            INSERT INTO aiu_presupuesto (
                id_presupuesto,
                costo_directo_total,
                total_administracion,
                porcentaje_administracion,
                total_imprevistos,
                porcentaje_imprevistos,
                total_utilidad,
                porcentaje_utilidad,
                iva_utilidad,
                porcentaje_iva_utilidad,
                total_aiu,
                porcentaje_total_aiu,
                valor_total_presupuesto
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            data["id_presupuesto"],
            data["costo_directo_total"],
            data["total_administracion"],
            data["porcentaje_administracion"],
            data["total_imprevistos"],
            data["porcentaje_imprevistos"],
            data["total_utilidad"],
            data["porcentaje_utilidad"],
            data["iva_utilidad"],
            data["porcentaje_iva_utilidad"],
            data["total_aiu"],
            data["porcentaje_total_aiu"],
            data["valor_total_presupuesto"]
        )
        return QueryExecutor.execute_return_id(query, params)

    def update_budget_totals(self, presupuesto_id, data):
        query = """
            UPDATE presupuestos
            SET
                total_administracion = %s,
                total_imprevistos = %s,
                total_utilidad = %s,
                iva_utilidad = %s,
                valor_total_presupuesto = %s
            WHERE id_presupuesto = %s;
        """
        params = (
            data["total_administracion"],
            data["total_imprevistos"],
            data["total_utilidad"],
            data["iva_utilidad"],
            data["valor_total_presupuesto"],
            presupuesto_id
        )
        return QueryExecutor.execute(query, params)