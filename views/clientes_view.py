import customtkinter as ctk

from controllers.cliente_controller import ClienteController
from views.components.base_table import BaseTable
from views.components.base_form import BaseForm
from utils.message_utils import MessageUtils


class ClientesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.controller = ClienteController()
        self.selected_id = None

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Gestión de Clientes",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Buscar cliente..."
        )
        self.search_entry.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search
        )
        search_btn.pack(side="left", padx=5)

        fields = [
            {"name": "tipo_cliente", "label": "Tipo Cliente", "type": "option", "values": ["persona_natural", "empresa_privada", "entidad_publica"]},
            {"name": "nombre_cliente", "label": "Nombre Cliente", "type": "entry"},
            {"name": "identificacion", "label": "Identificación", "type": "entry"},
            {"name": "telefono", "label": "Teléfono", "type": "entry"},
            {"name": "correo", "label": "Correo", "type": "entry"},
            {"name": "direccion", "label": "Dirección", "type": "entry"},
            {"name": "ciudad", "label": "Ciudad", "type": "entry"},
            {"name": "observaciones", "label": "Observaciones", "type": "textbox"}
        ]

        self.form = BaseForm(self, fields)
        self.form.pack(fill="x", padx=10, pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(button_frame, text="Guardar", command=self.save).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Actualizar", command=self.update).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Desactivar", command=self.disable).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

        columns = [
            "id_cliente",
            "tipo_cliente",
            "nombre_cliente",
            "identificacion",
            "telefono",
            "ciudad",
            "estado"
        ]

        headings = {
            "id_cliente": "ID",
            "tipo_cliente": "Tipo",
            "nombre_cliente": "Cliente",
            "identificacion": "Identificación",
            "telefono": "Teléfono",
            "ciudad": "Ciudad",
            "estado": "Estado"
        }

        self.table = BaseTable(self, columns, headings)
        self.table.pack(expand=True, fill="both", padx=10, pady=10)

        self.table.tree.bind("<<TreeviewSelect>>", self.on_select)
        
    def load_data(self):
        data = self.controller.load_clients()
        self.table.load_data(data)

    def search(self):
        text = self.search_entry.get()

        if not text:
            self.load_data()
            return

        data = self.controller.search_clients(text)
        self.table.load_data(data)

    def save(self):

        try:
            data = self.form.get_data()

            data["estado"] = "activo"

            self.controller.create_client(data)

            MessageUtils.success(
                "Cliente registrado correctamente."
            )

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update(self):

        if not self.selected_id:
            MessageUtils.warning(
                "Seleccione un cliente."
            )
            return

        try:
            data = self.form.get_data()

            self.controller.update_client(
                self.selected_id,
                data
            )

            MessageUtils.success(
                "Cliente actualizado."
            )

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable(self):

        if not self.selected_id:
            return

        confirm = MessageUtils.confirm(
            "¿Desea desactivar este cliente?"
        )

        if not confirm:
            return

        self.controller.disable_client(
            self.selected_id
        )

        MessageUtils.success(
            "Cliente desactivado."
        )

        self.clear()
        self.load_data()

    def clear(self):
        self.selected_id = None
        self.form.clear()

    def on_select(self, event):

        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]

        client = self.controller.get_client(
            self.selected_id
        )

        self.form.set_data(client)