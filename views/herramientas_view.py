import customtkinter as ctk

from controllers.herramienta_controller import HerramientaController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class HerramientasView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = HerramientaController()
        self.selected_id = None

        self.categories = []
        self.units = []

        self.category_options = []
        self.unit_options = []

        self.load_catalogs()

        self.create_widgets()
        self.load_data()

    def load_catalogs(self):

        self.categories = self.controller.get_active_categories()
        self.units = self.controller.get_active_units()

        self.category_map = {
            item["nombre_categoria"]: item["id_categoria_herramienta"]
            for item in self.categories
        }

        self.unit_map = {
            item["codigo_unidad"]: item["id_unidad"]
            for item in self.units
        }

        self.category_options = sorted(
            list(self.category_map.keys())
        )

        self.unit_options = sorted(
            list(self.unit_map.keys())
        )

        if not self.category_options:
            self.category_options = ["Sin categorías"]

        if not self.unit_options:
            self.unit_options = ["Sin unidades"]

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Gestión de Herramientas",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", padx=10)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=350,
            placeholder_text="Buscar..."
        )
        self.search_entry.pack(
            side="left",
            padx=5
        )

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
        form_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.create_label(
            form_frame,
            "Categoría",
            0,
            0
        )

        self.category_option = ctk.CTkOptionMenu(
            form_frame,
            values=self.category_options,
            width=250
        )

        self.category_option.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Unidad",
            0,
            2
        )

        self.unit_option = ctk.CTkOptionMenu(
            form_frame,
            values=self.unit_options,
            width=200
        )

        self.unit_option.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Código",
            1,
            0
        )

        self.codigo_entry = ctk.CTkEntry(
            form_frame,
            width=250
        )

        self.codigo_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Nombre",
            1,
            2
        )

        self.nombre_entry = ctk.CTkEntry(
            form_frame,
            width=300
        )

        self.nombre_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Valor Comercial",
            2,
            0
        )

        self.valor_entry = ctk.CTkEntry(
            form_frame,
            width=250
        )

        self.valor_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Rendimiento",
            2,
            2
        )

        self.rendimiento_entry = ctk.CTkEntry(
            form_frame,
            width=200
        )

        self.rendimiento_entry.grid(
            row=2,
            column=3,
            padx=5,
            pady=5
        )

        self.create_label(
            form_frame,
            "Número Herramientas",
            3,
            0
        )

        self.numero_entry = ctk.CTkEntry(
            form_frame,
            width=250
        )

        self.numero_entry.grid(
            row=3,
            column=1,
            padx=5,
            pady=5
        )

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

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
            "id_herramienta",
            "codigo_herramienta",
            "nombre_herramienta",
            "nombre_categoria",
            "codigo_unidad",
            "valor_comercial",
            "rendimiento",
            "numero_herramientas_obra",
            "valor_hora",
            "valor_por_obra"
        ]

        headings = {
            "id_herramienta": "ID",
            "codigo_herramienta": "Código",
            "nombre_herramienta": "Nombre",
            "nombre_categoria": "Categoría",
            "codigo_unidad": "Unidad",
            "valor_comercial": "Valor Comercial",
            "rendimiento": "Rendimiento",
            "numero_herramientas_obra": "Cant.",
            "valor_hora": "Valor Hora",
            "valor_por_obra": "Valor Obra"
        }

        self.table = BaseTable(
            self,
            columns,
            headings
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

    def create_label(
        self,
        master,
        text,
        row,
        column
    ):

        label = ctk.CTkLabel(
            master,
            text=text
        )

        label.grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="w"
        )

    def get_category_id(self):
        selected = self.category_option.get()

        if selected == "Sin categorías":
            return None

        return self.category_map.get(selected)

    def get_unit_id(self):
        selected = self.unit_option.get()

        if selected == "Sin unidades":
            return None

        return self.unit_map.get(selected)

    def get_form_data(self):

        return {
            "id_categoria_herramienta":
                self.get_category_id(),

            "id_unidad":
                self.get_unit_id(),

            "codigo_herramienta":
                self.codigo_entry.get(),

            "nombre_herramienta":
                self.nombre_entry.get(),

            "valor_comercial":
                self.valor_entry.get(),

            "rendimiento":
                self.rendimiento_entry.get(),

            "numero_herramientas_obra":
                self.numero_entry.get()
        }

    def format_currency(self, value):
        try:
            return (
                f"${float(value):,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
        except:
            return "$0,00"


    def format_money_fields(self, data):
        money_fields = [
            "valor_comercial",
            "valor_hora",
            "valor_por_obra"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data


    def load_data(self):

        data = self.controller.load_tools()
        data = self.format_money_fields(data)

        self.table.load_data(data)


    def search(self):

        text = self.search_entry.get()

        data = self.controller.search_tools(text)
        data = self.format_money_fields(data)

        self.table.load_data(data)

    def reload_all(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.clear()

        self.load_data()

    def save(self):

        try:

            self.controller.create_tool(
                self.get_form_data()
            )

            MessageUtils.success(
                "Herramienta creada correctamente."
            )

            self.clear()
            self.load_data()

        except Exception as error:

            MessageUtils.error(
                str(error)
            )

    def update(self):

        if not self.selected_id:

            MessageUtils.warning(
                "Seleccione un registro."
            )

            return

        try:

            self.controller.update_tool(
                self.selected_id,
                self.get_form_data()
            )

            MessageUtils.success(
                "Herramienta actualizada."
            )

            self.clear()
            self.load_data()

        except Exception as error:

            MessageUtils.error(
                str(error)
            )

    def disable(self):

        if not self.selected_id:

            MessageUtils.warning(
                "Seleccione un registro."
            )

            return

        confirm = MessageUtils.confirm(
            "¿Desea desactivar esta herramienta?"
        )

        if not confirm:
            return

        self.controller.disable_tool(
            self.selected_id
        )

        MessageUtils.success(
            "Herramienta desactivada."
        )

        self.clear()
        self.load_data()

    def clear(self):

        self.selected_id = None

        self.codigo_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.valor_entry.delete(0, "end")
        self.rendimiento_entry.delete(0, "end")
        self.numero_entry.delete(0, "end")

    def on_select(self, event):

        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]

        tool = self.controller.get_tool(
            self.selected_id
        )

        if not tool:
            return

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(
            0,
            tool["codigo_herramienta"]
        )

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(
            0,
            tool["nombre_herramienta"]
        )

        self.valor_entry.delete(0, "end")
        self.valor_entry.insert(
            0,
            tool["valor_comercial"]
        )

        self.rendimiento_entry.delete(0, "end")
        self.rendimiento_entry.insert(
            0,
            tool["rendimiento"]
        )

        self.numero_entry.delete(0, "end")
        self.numero_entry.insert(
            0,
            tool["numero_herramientas_obra"]
        )