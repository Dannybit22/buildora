from utils.security import Security
from database.query_executor import QueryExecutor


def crear_admin():
    password_hash = Security.hash_password("admin123")

    query = """
        INSERT INTO usuarios (
            id_rol,
            nombres,
            apellidos,
            correo,
            usuario,
            password_hash,
            estado
        )
        VALUES (
            1,
            'Administrador',
            'Buildora',
            'admin@buildora.com',
            'admin',
            %s,
            'activo'
        );
    """

    success = QueryExecutor.execute(query, (password_hash,))

    if success:
        print("Usuario administrador creado correctamente.")
        print("Usuario: admin")
        print("Contraseña: admin123")
    else:
        print("No se pudo crear el usuario administrador.")


if __name__ == "__main__":
    crear_admin()