import customtkinter as ctk

from controllers.material_controller import MaterialController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class MaterialesView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = MaterialController()
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
            cat["nombre_categoria"]: cat["id_categoria_material"]
            for cat in self.categories
        }

        self.unit_map = {
            unit["codigo_unidad"]: unit["id_unidad"]
            for unit in self.units
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
            text="Gestión de Materiales",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=360,
            placeholder_text="Buscar por código, descripción, categoría o unidad..."
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

        self.create_label(form_frame, "Categoría", 0, 0)
        self.category_option = ctk.CTkOptionMenu(
            form_frame,
            width=260,
            values=self.category_options
        )
        self.category_option.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Unidad", 0, 2)
        self.unit_option = ctk.CTkOptionMenu(
            form_frame,
            width=220,
            values=self.unit_options
        )
        self.unit_option.grid(row=0, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Código", 1, 0)
        self.codigo_entry = ctk.CTkEntry(form_frame, width=260)
        self.codigo_entry.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Descripción", 1, 2)
        self.descripcion_entry = ctk.CTkEntry(form_frame, width=320)
        self.descripcion_entry.grid(row=1, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Valor empaque", 2, 0)
        self.valor_empaque_entry = ctk.CTkEntry(form_frame, width=260)
        self.valor_empaque_entry.grid(row=2, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Cant. por empaque", 2, 2)
        self.cantidad_empaque_entry = ctk.CTkEntry(form_frame, width=220)
        self.cantidad_empaque_entry.grid(row=2, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Rendimiento", 3, 0)
        self.rendimiento_entry = ctk.CTkEntry(form_frame, width=260)
        self.rendimiento_entry.grid(row=3, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "% Desperdicio", 3, 2)
        self.desperdicio_entry = ctk.CTkEntry(form_frame, width=220)
        self.desperdicio_entry.grid(row=3, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Unidad cotización", 4, 0)
        self.unidad_cotizacion_entry = ctk.CTkEntry(form_frame, width=260)
        self.unidad_cotizacion_entry.grid(row=4, column=1, padx=8, pady=6, sticky="w")

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
            "id_material",
            "codigo_material",
            "descripcion",
            "nombre_categoria",
            "codigo_unidad",
            "precio_por_unidad",
            "rendimiento",
            "porcentaje_desperdicio",
            "valor_total",
            "estado"
        ]

        headings = {
            "id_material": "ID",
            "codigo_material": "Código",
            "descripcion": "Descripción",
            "nombre_categoria": "Categoría",
            "codigo_unidad": "Unidad",
            "precio_por_unidad": "Precio Unit.",
            "rendimiento": "Rend.",
            "porcentaje_desperdicio": "% Desp.",
            "valor_total": "Valor Total",
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

    def get_selected_category_id(self):
        selected = self.category_option.get()

        if selected == "Sin categorías":
            return None

        return self.category_map.get(selected)

    def get_selected_unit_id(self):
        selected = self.unit_option.get()

        if selected == "Sin unidades":
            return None

        return self.unit_map.get(selected)

    def set_category_option_by_id(self, category_id):
        if category_id is None:
            return

        for name, id_value in self.category_map.items():
            if id_value == category_id:
                self.category_option.set(name)
                return

    def set_unit_option_by_id(self, unit_id):
        if unit_id is None:
            return

        for code, id_value in self.unit_map.items():
            if id_value == unit_id:
                self.unit_option.set(code)
                return

    def get_form_data(self):
        return {
            "id_categoria_material": self.get_selected_category_id(),
            "id_unidad": self.get_selected_unit_id(),
            "codigo_material": self.codigo_entry.get().strip(),
            "descripcion": self.descripcion_entry.get().strip(),
            "valor_comercial_empaque": self.valor_empaque_entry.get().strip(),
            "cantidad_por_empaque": self.cantidad_empaque_entry.get().strip(),
            "rendimiento": self.rendimiento_entry.get().strip(),
            "porcentaje_desperdicio": self.desperdicio_entry.get().strip(),
            "unidad_cotizacion": self.unidad_cotizacion_entry.get().strip(),
            "estado": "activo"
        }

    def load_data(self):
        data = self.controller.load_materials()

        for item in data:
            try:
                item["precio_por_unidad"] = (
                    f"${float(item['precio_por_unidad']):,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            except:
                pass

            try:
                item["valor_total"] = (
                    f"${float(item['valor_total']):,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            except:
                pass

        self.table.load_data(data)
        
    def search(self):
        text = self.search_entry.get().strip()

        if not text:
            self.load_data()
            return

        data = self.controller.search_materials(text)

        for item in data:
            try:
                item["precio_por_unidad"] = (
                    f"${float(item['precio_por_unidad']):,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            except:
                pass

            try:
                item["valor_total"] = (
                    f"${float(item['valor_total']):,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            except:
                pass

        self.table.load_data(data)

    def reload_all(self):
        self.load_catalogs()
        self.category_option.configure(values=self.category_options)
        self.unit_option.configure(values=self.unit_options)

        if self.category_options:
            self.category_option.set(self.category_options[0])

        if self.unit_options:
            self.unit_option.set(self.unit_options[0])

        self.search_entry.delete(0, "end")
        self.clear()
        self.load_data()

    def save(self):
        try:
            data = self.get_form_data()
            self.controller.create_material(data)

            MessageUtils.success("Material registrado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un material.")
            return

        try:
            data = self.get_form_data()
            self.controller.update_material(self.selected_id, data)

            MessageUtils.success("Material actualizado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un material.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea desactivar este material?"
        )

        if not confirm:
            return

        self.controller.disable_material(self.selected_id)

        MessageUtils.success("Material desactivado correctamente.")

        self.clear()
        self.load_data()

    def clear(self):
        self.selected_id = None

        if self.category_options:
            self.category_option.set(self.category_options[0])

        if self.unit_options:
            self.unit_option.set(self.unit_options[0])

        self.codigo_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        self.valor_empaque_entry.delete(0, "end")
        self.cantidad_empaque_entry.delete(0, "end")
        self.rendimiento_entry.delete(0, "end")
        self.desperdicio_entry.delete(0, "end")
        self.unidad_cotizacion_entry.delete(0, "end")

    def on_select(self, event):
        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]
        material = self.controller.get_material(self.selected_id)

        if not material:
            return

        self.set_category_option_by_id(material.get("id_categoria_material"))
        self.set_unit_option_by_id(material.get("id_unidad"))

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, material.get("codigo_material") or "")

        self.descripcion_entry.delete(0, "end")
        self.descripcion_entry.insert(0, material.get("descripcion") or "")

        self.valor_empaque_entry.delete(0, "end")
        self.valor_empaque_entry.insert(0, str(material.get("valor_comercial_empaque") or ""))

        self.cantidad_empaque_entry.delete(0, "end")
        self.cantidad_empaque_entry.insert(0, str(material.get("cantidad_por_empaque") or ""))

        self.rendimiento_entry.delete(0, "end")
        self.rendimiento_entry.insert(0, str(material.get("rendimiento") or ""))

        self.desperdicio_entry.delete(0, "end")
        self.desperdicio_entry.insert(0, str(material.get("porcentaje_desperdicio") or ""))

        self.unidad_cotizacion_entry.delete(0, "end")
        self.unidad_cotizacion_entry.insert(0, material.get("unidad_cotizacion") or "")