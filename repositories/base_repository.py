from database.query_executor import QueryExecutor


class BaseRepository:
    def __init__(self, table_name, primary_key, fields, search_fields=None):
        self.table_name = table_name
        self.primary_key = primary_key
        self.fields = fields
        self.search_fields = search_fields or []

    def get_all(self, only_active=True):
        query = f"SELECT * FROM {self.table_name}"

        if only_active:
            query += " WHERE estado = 'activo'"

        query += f" ORDER BY {self.primary_key} DESC"

        return QueryExecutor.fetch_all(query)

    def get_by_id(self, record_id):
        query = f"""
            SELECT *
            FROM {self.table_name}
            WHERE {self.primary_key} = %s
            LIMIT 1
        """
        return QueryExecutor.fetch_one(query, (record_id,))

    def search(self, search_text):
        if not self.search_fields:
            return self.get_all()

        conditions = []
        params = []

        for field in self.search_fields:
            conditions.append(f"{field} LIKE %s")
            params.append(f"%{search_text}%")

        query = f"""
            SELECT *
            FROM {self.table_name}
            WHERE estado = 'activo'
            AND ({' OR '.join(conditions)})
            ORDER BY {self.primary_key} DESC
        """

        return QueryExecutor.fetch_all(query, tuple(params))

    def create(self, data):
        clean_data = {
            key: value
            for key, value in data.items()
            if key in self.fields
        }

        columns = ", ".join(clean_data.keys())
        placeholders = ", ".join(["%s"] * len(clean_data))
        values = tuple(clean_data.values())

        query = f"""
            INSERT INTO {self.table_name} ({columns})
            VALUES ({placeholders})
        """

        return QueryExecutor.execute_return_id(query, values)

    def update(self, record_id, data):
        clean_data = {
            key: value
            for key, value in data.items()
            if key in self.fields
        }

        set_clause = ", ".join([f"{key} = %s" for key in clean_data.keys()])
        values = tuple(clean_data.values()) + (record_id,)

        query = f"""
            UPDATE {self.table_name}
            SET {set_clause}
            WHERE {self.primary_key} = %s
        """

        return QueryExecutor.execute(query, values)

    def disable(self, record_id):
        query = f"""
            UPDATE {self.table_name}
            SET estado = 'inactivo'
            WHERE {self.primary_key} = %s
        """
        return QueryExecutor.execute(query, (record_id,))