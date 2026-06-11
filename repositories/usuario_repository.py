from database.query_executor import QueryExecutor


class UsuarioRepository:
    @staticmethod
    def find_by_username(username: str):
        query = """
            SELECT 
                u.id_usuario,
                u.id_rol,
                r.nombre_rol,
                u.nombres,
                u.apellidos,
                u.correo,
                u.usuario,
                u.password_hash,
                u.estado
            FROM usuarios u
            INNER JOIN roles r ON u.id_rol = r.id_rol
            WHERE u.usuario = %s
            LIMIT 1;
        """

        return QueryExecutor.fetch_one(query, (username,))

    @staticmethod
    def update_last_access(id_usuario: int):
        query = """
            UPDATE usuarios
            SET ultimo_acceso = NOW()
            WHERE id_usuario = %s;
        """

        return QueryExecutor.execute(query, (id_usuario,))