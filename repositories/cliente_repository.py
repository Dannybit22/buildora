from repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            table_name="clientes",
            primary_key="id_cliente",
            fields=[
                "tipo_cliente",
                "nombre_cliente",
                "identificacion",
                "telefono",
                "correo",
                "direccion",
                "ciudad",
                "observaciones",
                "estado"
            ],
            search_fields=[
                "nombre_cliente",
                "identificacion",
                "ciudad"
            ]
        )