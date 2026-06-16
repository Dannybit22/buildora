import customtkinter as ctk

from controllers.proyecto_controller import ProyectoController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class ProyectosView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = ProyectoController()
        self.selected_id = None
        self.clients = []
        self.client_options = []

        self.load_clients()
        self.create_widgets()
        self.load_data()

    def load_clients(self):
        self.clients = self.controller.get_active_clients()

        self.client_options = [
            f"{client['id_cliente']} - {client['nombre_cliente']}"
            for client in self.clients
        ]

        if not self.client_options:
            self.client_options = ["Sin clientes activos"]

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Gestión de Proyectos",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=320,
            placeholder_text="Buscar por código, proyecto, ubicación o cliente..."
        )
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Buscar",
            command=self.search
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Recargar",
            command=self.reload_all
        ).pack(side="left", padx=5)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.client_option = ctk.CTkOptionMenu(
            form_frame,
            width=300,
            values=self.client_options
        )
        self.create_label(form_frame, "Cliente", 0, 0)
        self.client_option.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        self.codigo_entry = ctk.CTkEntry(form_frame, width=260)
        self.create_label(form_frame, "Código Proyecto", 0, 2)
        self.codigo_entry.grid(row=0, column=3, padx=8, pady=6, sticky="w")

        self.nombre_entry = ctk.CTkEntry(form_frame, width=300)
        self.create_label(form_frame, "Nombre Proyecto", 1, 0)
        self.nombre_entry.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        self.ubicacion_entry = ctk.CTkEntry(form_frame, width=260)
        self.create_label(form_frame, "Ubicación", 1, 2)
        self.ubicacion_entry.grid(row=1, column=3, padx=8, pady=6, sticky="w")

        self.fecha_entry = ctk.CTkEntry(
            form_frame,
            width=260,
            placeholder_text="AAAA-MM-DD"
        )
        self.create_label(form_frame, "Fecha", 2, 0)
        self.fecha_entry.grid(row=2, column=1, padx=8, pady=6, sticky="w")

        self.descripcion_text = ctk.CTkTextbox(form_frame, width=300, height=70)
        self.create_label(form_frame, "Descripción", 3, 0)
        self.descripcion_text.grid(row=3, column=1, padx=8, pady=6, sticky="w")

        self.observaciones_text = ctk.CTkTextbox(form_frame, width=300, height=70)
        self.create_label(form_frame, "Observaciones", 3, 2)
        self.observaciones_text.grid(row=3, column=3, padx=8, pady=6, sticky="w")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            button_frame,
            text="Guardar",
            command=self.save
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Actualizar",
            command=self.update
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Desactivar",
            command=self.disable
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Limpiar",
            command=self.clear
        ).pack(side="left", padx=5)

        columns = [
            "id_proyecto",
            "codigo_proyecto",
            "nombre_proyecto",
            "nombre_cliente",
            "ubicacion",
            "fecha_proyecto",
            "estado"
        ]

        headings = {
            "id_proyecto": "ID",
            "codigo_proyecto": "Código",
            "nombre_proyecto": "Proyecto",
            "nombre_cliente": "Cliente",
            "ubicacion": "Ubicación",
            "fecha_proyecto": "Fecha",
            "estado": "Estado"
        }

        self.table = BaseTable(self, columns, headings)
        self.table.pack(expand=True, fill="both", padx=10, pady=10)

        self.table.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_label(self, master, text, row, column):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=("Arial", 12, "bold")
        )
        label.grid(row=row, column=column, padx=8, pady=6, sticky="w")

    def get_selected_client_id(self):
        selected = self.client_option.get()

        if selected == "Sin clientes activos":
            return None

        try:
            return int(selected.split(" - ")[0])
        except Exception:
            return None

    def set_client_option_by_id(self, id_cliente):
        for option in self.client_options:
            if option.startswith(f"{id_cliente} - "):
                self.client_option.set(option)
                return

    def get_form_data(self):
        return {
            "id_cliente": self.get_selected_client_id(),
            "codigo_proyecto": self.codigo_entry.get().strip(),
            "nombre_proyecto": self.nombre_entry.get().strip(),
            "ubicacion": self.ubicacion_entry.get().strip(),
            "fecha_proyecto": self.fecha_entry.get().strip(),
            "descripcion": self.descripcion_text.get("1.0", "end").strip(),
            "observaciones": self.observaciones_text.get("1.0", "end").strip(),
            "estado": "activo"
        }

    def load_data(self):
        data = self.controller.load_projects()
        self.table.load_data(data)

    def search(self):
        text = self.search_entry.get().strip()

        if not text:
            self.load_data()
            return

        data = self.controller.search_projects(text)
        self.table.load_data(data)

    def reload_all(self):
        self.load_clients()
        self.client_option.configure(values=self.client_options)
        if self.client_options:
            self.client_option.set(self.client_options[0])

        self.search_entry.delete(0, "end")
        self.clear()
        self.load_data()

    def save(self):
        try:
            data = self.get_form_data()
            self.controller.create_project(data)

            MessageUtils.success("Proyecto registrado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un proyecto.")
            return

        try:
            data = self.get_form_data()
            self.controller.update_project(self.selected_id, data)

            MessageUtils.success("Proyecto actualizado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un proyecto.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea desactivar este proyecto?"
        )

        if not confirm:
            return

        self.controller.disable_project(self.selected_id)

        MessageUtils.success("Proyecto desactivado correctamente.")

        self.clear()
        self.load_data()

    def clear(self):
        self.selected_id = None

        if self.client_options:
            self.client_option.set(self.client_options[0])

        self.codigo_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.ubicacion_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")

        self.descripcion_text.delete("1.0", "end")
        self.observaciones_text.delete("1.0", "end")

    def on_select(self, event):
        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]

        project = self.controller.get_project(self.selected_id)

        if not project:
            return

        self.set_client_option_by_id(project["id_cliente"])

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, project.get("codigo_proyecto") or "")

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, project.get("nombre_proyecto") or "")

        self.ubicacion_entry.delete(0, "end")
        self.ubicacion_entry.insert(0, project.get("ubicacion") or "")

        self.fecha_entry.delete(0, "end")
        self.fecha_entry.insert(0, str(project.get("fecha_proyecto") or ""))

        self.descripcion_text.delete("1.0", "end")
        self.descripcion_text.insert("1.0", project.get("descripcion") or "")

        self.observaciones_text.delete("1.0", "end")
        self.observaciones_text.insert("1.0", project.get("observaciones") or "")