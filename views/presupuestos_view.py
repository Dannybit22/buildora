import customtkinter as ctk

from controllers.presupuesto_controller import PresupuestoController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class PresupuestosView(ctk.CTkFrame):

    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")

        self.controller = PresupuestoController()
        self.user = user

        self.selected_id = None
        self.selected_capitulo_id = None
        self.selected_item_id = None

        self.projects = []
        self.project_options = []

        self.apus = []
        self.apu_options = []

        self.load_catalogs()
        self.create_widgets()
        self.load_data()

    def load_catalogs(self):
        self.projects = self.controller.get_all_projects()
        self.apus = self.controller.get_apus()

        self.project_options = [
            f"{p['id_proyecto']} - {p['codigo_proyecto']} - {p['nombre_proyecto']}"
            for p in self.projects
        ]

        self.apu_options = [
            f"{a['id_apu']} - {a['codigo_apu']} - {a['descripcion']}"
            for a in self.apus
        ]

        if not self.project_options:
            self.project_options = ["Sin proyectos activos"]

        if not self.apu_options:
            self.apu_options = ["Sin APUs activos"]

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Gestión de Presupuestos",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=8)

        self.create_budget_section()
        self.create_chapter_section()
        self.create_item_section()

    def create_budget_section(self):
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=4)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=420,
            placeholder_text="Buscar presupuesto..."
        )
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="Buscar", command=self.search).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Recargar", command=self.reload_all).pack(side="left", padx=5)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        self.create_label(form_frame, "Proyecto", 0, 0)
        self.project_option = ctk.CTkOptionMenu(
            form_frame,
            width=430,
            values=self.project_options
        )
        self.project_option.grid(row=0, column=1, columnspan=3, padx=8, pady=4, sticky="w")

        self.create_label(form_frame, "Código", 1, 0)
        self.codigo_entry = ctk.CTkEntry(form_frame, width=220)
        self.codigo_entry.grid(row=1, column=1, padx=8, pady=4, sticky="w")

        self.create_label(form_frame, "Nombre", 1, 2)
        self.nombre_entry = ctk.CTkEntry(form_frame, width=300)
        self.nombre_entry.grid(row=1, column=3, padx=8, pady=4, sticky="w")

        self.create_label(form_frame, "Fecha", 2, 0)
        self.fecha_entry = ctk.CTkEntry(form_frame, width=220, placeholder_text="AAAA-MM-DD")
        self.fecha_entry.grid(row=2, column=1, padx=8, pady=4, sticky="w")

        self.create_label(form_frame, "Descripción", 2, 2)
        self.descripcion_entry = ctk.CTkEntry(form_frame, width=300)
        self.descripcion_entry.grid(row=2, column=3, padx=8, pady=4, sticky="w")

        self.create_label(form_frame, "Observaciones", 3, 0)
        self.observaciones_entry = ctk.CTkEntry(form_frame, width=430)
        self.observaciones_entry.grid(row=3, column=1, columnspan=3, padx=8, pady=4, sticky="w")

        totals_frame = ctk.CTkFrame(self)
        totals_frame.pack(fill="x", padx=10, pady=4)

        self.lbl_costo_directo = self.create_total_label(totals_frame, "Costo directo: $0", 0)
        self.lbl_admin = self.create_total_label(totals_frame, "Administración: $0", 1)
        self.lbl_imprevistos = self.create_total_label(totals_frame, "Imprevistos: $0", 2)
        self.lbl_utilidad = self.create_total_label(totals_frame, "Utilidad: $0", 3)
        self.lbl_total = self.create_total_label(totals_frame, "Total: $0", 4)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=4)

        ctk.CTkButton(button_frame, text="Guardar Presupuesto", command=self.save_budget).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Actualizar Presupuesto", command=self.update_budget).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cerrar Presupuesto", command=self.close_budget).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Limpiar", command=self.clear_all).pack(side="left", padx=5)

        columns = [
            "id_presupuesto",
            "codigo_presupuesto",
            "nombre_presupuesto",
            "nombre_proyecto",
            "nombre_cliente",
            "fecha_presupuesto",
            "costo_directo_total",
            "valor_total_presupuesto",
            "estado"
        ]

        headings = {
            "id_presupuesto": "ID",
            "codigo_presupuesto": "Código",
            "nombre_presupuesto": "Presupuesto",
            "nombre_proyecto": "Proyecto",
            "nombre_cliente": "Cliente",
            "fecha_presupuesto": "Fecha",
            "costo_directo_total": "Costo Directo",
            "valor_total_presupuesto": "Total",
            "estado": "Estado"
        }

        self.budget_table = BaseTable(self, columns, headings)
        self.budget_table.tree.configure(height=3)
        self.budget_table.pack(fill="x", expand=False, padx=10, pady=5)
        self.budget_table.tree.bind("<<TreeviewSelect>>", self.on_select_budget)
    
    def create_chapter_section(self):
        section = ctk.CTkFrame(self)
        section.pack(fill="x", padx=10, pady=5)

        title = ctk.CTkLabel(section, text="Capítulos del Presupuesto", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=6, padx=8, pady=4, sticky="w")

        self.create_label(section, "Código", 1, 0)
        self.cap_codigo_entry = ctk.CTkEntry(section, width=140)
        self.cap_codigo_entry.grid(row=1, column=1, padx=5, pady=4)

        self.create_label(section, "Nombre", 1, 2)
        self.cap_nombre_entry = ctk.CTkEntry(section, width=260)
        self.cap_nombre_entry.grid(row=1, column=3, padx=5, pady=4)

        self.create_label(section, "Orden", 1, 4)
        self.cap_orden_entry = ctk.CTkEntry(section, width=80)
        self.cap_orden_entry.grid(row=1, column=5, padx=5, pady=4)
        self.cap_orden_entry.insert(0, "1")

        self.create_label(section, "Descripción", 2, 0)
        self.cap_descripcion_entry = ctk.CTkEntry(section, width=430)
        self.cap_descripcion_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=4, sticky="w")

        ctk.CTkButton(section, text="Agregar Capítulo", command=self.save_chapter).grid(row=2, column=4, padx=5)
        ctk.CTkButton(section, text="Actualizar", command=self.update_chapter).grid(row=2, column=5, padx=5)
        ctk.CTkButton(section, text="Quitar", command=self.disable_chapter).grid(row=2, column=6, padx=5)

        columns = [
            "id_capitulo",
            "codigo_capitulo",
            "nombre_capitulo",
            "orden",
            "costo_total_capitulo",
            "porcentaje_participacion"
        ]

        headings = {
            "id_capitulo": "ID",
            "codigo_capitulo": "Código",
            "nombre_capitulo": "Capítulo",
            "orden": "Orden",
            "costo_total_capitulo": "Total",
            "porcentaje_participacion": "%"
        }

        self.chapters_table = BaseTable(section, columns, headings)
        self.chapters_table.tree.configure(height=3)
        self.chapters_table.grid(row=3, column=0, columnspan=7, sticky="ew", padx=5, pady=5)
        self.chapters_table.tree.bind("<<TreeviewSelect>>", self.on_select_chapter)

    def create_item_section(self):
        section = ctk.CTkFrame(self)
        section.pack(fill="both", expand=True, padx=10, pady=5)

        title = ctk.CTkLabel(section, text="Ítems del Capítulo", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=6, padx=8, pady=4, sticky="w")

        self.create_label(section, "APU", 1, 0)
        self.apu_option = ctk.CTkOptionMenu(section, width=430, values=self.apu_options)
        self.apu_option.grid(row=1, column=1, columnspan=4, padx=5, pady=4, sticky="w")

        self.create_label(section, "Código Ítem", 2, 0)
        self.item_codigo_entry = ctk.CTkEntry(section, width=140)
        self.item_codigo_entry.grid(row=2, column=1, padx=5, pady=4)

        self.create_label(section, "Descripción", 2, 2)
        self.item_descripcion_entry = ctk.CTkEntry(section, width=260)
        self.item_descripcion_entry.grid(row=2, column=3, padx=5, pady=4)

        self.create_label(section, "Cantidad", 3, 0)
        self.item_cantidad_entry = ctk.CTkEntry(section, width=140)
        self.item_cantidad_entry.grid(row=3, column=1, padx=5, pady=4)
        self.item_cantidad_entry.insert(0, "1")

        self.create_label(section, "Orden", 3, 2)
        self.item_orden_entry = ctk.CTkEntry(section, width=100)
        self.item_orden_entry.grid(row=3, column=3, padx=5, pady=4)
        self.item_orden_entry.insert(0, "1")

        ctk.CTkButton(section, text="Agregar Ítem desde APU", command=self.add_item).grid(row=3, column=4, padx=5)
        ctk.CTkButton(section, text="Actualizar Cantidad", command=self.update_item_quantity).grid(row=3, column=5, padx=5)
        ctk.CTkButton(section, text="Quitar Ítem", command=self.disable_item).grid(row=3, column=6, padx=5)

        columns = [
            "id_item",
            "codigo_item",
            "descripcion_item",
            "unidad_item",
            "cantidad",
            "costo_unitario_historico",
            "costo_total_item",
            "codigo_apu_historico"
        ]

        headings = {
            "id_item": "ID",
            "codigo_item": "Código",
            "descripcion_item": "Ítem",
            "unidad_item": "Unidad",
            "cantidad": "Cantidad",
            "costo_unitario_historico": "Vr. Unit.",
            "costo_total_item": "Total",
            "codigo_apu_historico": "APU"
        }

        self.items_table = BaseTable(section, columns, headings)
        self.items_table.tree.configure(height=3)
        self.items_table.grid(row=4, column=0, columnspan=7, sticky="ew", padx=5, pady=5)
        self.items_table.tree.bind("<<TreeviewSelect>>", self.on_select_item)

        section.grid_columnconfigure(1, weight=1)
        section.grid_columnconfigure(3, weight=1)
        
    def create_label(self, master, text, row, column):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=("Arial", 12, "bold")
        )
        label.grid(row=row, column=column, padx=8, pady=4, sticky="w")

    def create_total_label(self, master, text, column):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=("Arial", 12, "bold")
        )
        label.grid(row=0, column=column, padx=12, pady=6, sticky="w")
        return label

    def get_id_from_option(self, option_text, empty_text):
        if option_text == empty_text:
            return None

        try:
            return int(option_text.split(" - ")[0])
        except Exception:
            return None

    def get_selected_project_id(self):
        return self.get_id_from_option(
            self.project_option.get(),
            "Sin proyectos activos"
        )

    def get_selected_apu_id(self):
        return self.get_id_from_option(
            self.apu_option.get(),
            "Sin APUs activos"
        )

    def set_project_option_by_id(self, project_id):
        for option in self.project_options:
            if option.startswith(f"{project_id} - "):
                self.project_option.set(option)
                return

    def get_budget_form_data(self):
        return {
            "id_proyecto": self.get_selected_project_id(),
            "id_usuario_creador": self.user["id_usuario"],
            "codigo_presupuesto": self.codigo_entry.get().strip(),
            "nombre_presupuesto": self.nombre_entry.get().strip(),
            "descripcion": self.descripcion_entry.get().strip(),
            "fecha_presupuesto": self.fecha_entry.get().strip(),
            "costo_directo_total": 0,
            "total_administracion": 0,
            "total_imprevistos": 0,
            "total_utilidad": 0,
            "iva_utilidad": 0,
            "valor_total_presupuesto": 0,
            "estado": "borrador",
            "observaciones": self.observaciones_entry.get().strip()
        }

    def get_chapter_form_data(self):
        return {
            "id_presupuesto": self.selected_id,
            "codigo_capitulo": self.cap_codigo_entry.get().strip(),
            "nombre_capitulo": self.cap_nombre_entry.get().strip(),
            "descripcion": self.cap_descripcion_entry.get().strip(),
            "orden": self.cap_orden_entry.get().strip(),
            "estado": "activo"
        }

    def get_item_form_data(self):
        return {
            "id_capitulo": self.selected_capitulo_id,
            "id_apu": self.get_selected_apu_id(),
            "codigo_item": self.item_codigo_entry.get().strip(),
            "descripcion_item": self.item_descripcion_entry.get().strip(),
            "cantidad": self.item_cantidad_entry.get().strip(),
            "orden": self.item_orden_entry.get().strip()
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

    def format_budgets(self, data):

        money_fields = [
            "costo_directo_total",
            "valor_total_presupuesto"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data


    def format_chapters(self, data):

        for item in data:
            if "costo_total_capitulo" in item:
                item["costo_total_capitulo"] = self.format_currency(
                    item["costo_total_capitulo"]
                )

        return data


    def format_items(self, data):

        money_fields = [
            "costo_unitario_historico",
            "costo_total_item"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data
        
    def load_data(self):
        data = self.controller.load_budgets()
        data = self.format_budgets(data)

        self.budget_table.load_data(data)

    def search(self):
        text = self.search_entry.get().strip()

        if not text:
            self.load_data()
            return

        data = self.controller.search_budgets(text)
        data = self.format_budgets(data)

        self.budget_table.load_data(data)

    def reload_all(self):
        self.load_catalogs()

        self.project_option.configure(values=self.project_options)
        self.apu_option.configure(values=self.apu_options)

        self.clear_all()
        self.load_data()

    def save_budget(self):
        try:
            budget_id = self.controller.create_budget(
                self.get_budget_form_data()
            )

            MessageUtils.success("Presupuesto creado correctamente.")

            self.clear_all()
            self.load_data()

            self.selected_id = budget_id

        except Exception as error:
            MessageUtils.error(str(error))

    def update_budget(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un presupuesto.")
            return

        try:
            current = self.controller.get_budget(self.selected_id)

            if not current:
                MessageUtils.error("No se encontró el presupuesto.")
                return

            data = self.get_budget_form_data()

            data["costo_directo_total"] = current.get("costo_directo_total") or 0
            data["total_administracion"] = current.get("total_administracion") or 0
            data["total_imprevistos"] = current.get("total_imprevistos") or 0
            data["total_utilidad"] = current.get("total_utilidad") or 0
            data["iva_utilidad"] = current.get("iva_utilidad") or 0
            data["valor_total_presupuesto"] = current.get("valor_total_presupuesto") or 0
            data["estado"] = current.get("estado") or "borrador"

            self.controller.update_budget(self.selected_id, data)

            MessageUtils.success("Presupuesto actualizado correctamente.")

            self.load_data()
            self.refresh_selected_budget()

        except Exception as error:
            MessageUtils.error(str(error))

    def close_budget(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un presupuesto.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea cerrar este presupuesto?"
        )

        if not confirm:
            return

        self.controller.close_budget(self.selected_id)

        MessageUtils.success("Presupuesto cerrado correctamente.")

        self.clear_all()
        self.load_data()

    def save_chapter(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione primero un presupuesto.")
            return

        try:
            self.controller.create_chapter(
                self.get_chapter_form_data()
            )

            MessageUtils.success("Capítulo creado correctamente.")

            self.clear_chapter_form()
            self.refresh_chapters()
            self.refresh_selected_budget()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update_chapter(self):
        if not self.selected_capitulo_id:
            MessageUtils.warning("Seleccione un capítulo.")
            return

        try:
            self.controller.update_chapter(
                self.selected_capitulo_id,
                self.get_chapter_form_data()
            )

            MessageUtils.success("Capítulo actualizado correctamente.")

            self.clear_chapter_form()
            self.refresh_chapters()
            self.refresh_selected_budget()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable_chapter(self):
        if not self.selected_capitulo_id:
            MessageUtils.warning("Seleccione un capítulo.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea quitar este capítulo?"
        )

        if not confirm:
            return

        self.controller.disable_chapter(self.selected_capitulo_id)

        MessageUtils.success("Capítulo desactivado correctamente.")

        self.selected_capitulo_id = None
        self.clear_chapter_form()
        self.items_table.clear()
        self.refresh_chapters()
        self.refresh_selected_budget()
        self.load_data()

    def add_item(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione primero un presupuesto.")
            return

        if not self.selected_capitulo_id:
            MessageUtils.warning("Seleccione primero un capítulo.")
            return

        try:
            self.controller.create_item_from_apu(
                self.get_item_form_data()
            )

            MessageUtils.success("Ítem agregado correctamente.")

            self.clear_item_form()
            self.refresh_items()
            self.refresh_chapters()
            self.refresh_selected_budget()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update_item_quantity(self):
        if not self.selected_item_id:
            MessageUtils.warning("Seleccione un ítem.")
            return

        try:
            data = {
                "cantidad": self.item_cantidad_entry.get().strip()
            }

            self.controller.update_item_quantity(
                self.selected_item_id,
                data
            )

            MessageUtils.success("Cantidad actualizada correctamente.")

            self.clear_item_form()
            self.refresh_items()
            self.refresh_chapters()
            self.refresh_selected_budget()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable_item(self):
        if not self.selected_item_id:
            MessageUtils.warning("Seleccione un ítem.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea quitar este ítem?"
        )

        if not confirm:
            return

        self.controller.disable_item(self.selected_item_id)

        MessageUtils.success("Ítem desactivado correctamente.")

        self.selected_item_id = None
        self.clear_item_form()
        self.refresh_items()
        self.refresh_chapters()
        self.refresh_selected_budget()
        self.load_data()

    def on_select_budget(self, event):
        values = self.budget_table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]
        self.selected_capitulo_id = None
        self.selected_item_id = None

        self.refresh_selected_budget()
        self.refresh_chapters()
        self.items_table.clear()

    def on_select_chapter(self, event):
        values = self.chapters_table.get_selected_values()

        if not values:
            return

        self.selected_capitulo_id = values[0]
        self.selected_item_id = None

        chapter = None
        chapters = self.controller.get_chapters(self.selected_id)

        for item in chapters:
            if item["id_capitulo"] == self.selected_capitulo_id:
                chapter = item
                break

        if chapter:
            self.cap_codigo_entry.delete(0, "end")
            self.cap_codigo_entry.insert(0, chapter.get("codigo_capitulo") or "")

            self.cap_nombre_entry.delete(0, "end")
            self.cap_nombre_entry.insert(0, chapter.get("nombre_capitulo") or "")

            self.cap_orden_entry.delete(0, "end")
            self.cap_orden_entry.insert(0, str(chapter.get("orden") or "1"))

            self.cap_descripcion_entry.delete(0, "end")
            self.cap_descripcion_entry.insert(0, chapter.get("descripcion") or "")

        self.refresh_items()

    def on_select_item(self, event):
        values = self.items_table.get_selected_values()

        if not values:
            return

        self.selected_item_id = values[0]

        item_id = values[0]
        items = self.controller.get_items_by_chapter(self.selected_capitulo_id)

        selected_item = None

        for item in items:
            if item["id_item"] == item_id:
                selected_item = item
                break

        if not selected_item:
            return

        self.item_codigo_entry.delete(0, "end")
        self.item_codigo_entry.insert(0, selected_item.get("codigo_item") or "")

        self.item_descripcion_entry.delete(0, "end")
        self.item_descripcion_entry.insert(0, selected_item.get("descripcion_item") or "")

        self.item_cantidad_entry.delete(0, "end")
        self.item_cantidad_entry.insert(0, str(selected_item.get("cantidad") or "1"))

        self.item_orden_entry.delete(0, "end")
        self.item_orden_entry.insert(0, str(selected_item.get("orden") or "1"))

    def refresh_selected_budget(self):
        if not self.selected_id:
            return

        budget = self.controller.get_budget(self.selected_id)

        if not budget:
            return

        self.set_project_option_by_id(budget.get("id_proyecto"))

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, budget.get("codigo_presupuesto") or "")

        self.nombre_entry.delete(0, "end")
        self.nombre_entry.insert(0, budget.get("nombre_presupuesto") or "")

        self.fecha_entry.delete(0, "end")
        self.fecha_entry.insert(0, str(budget.get("fecha_presupuesto") or ""))

        self.descripcion_entry.delete(0, "end")
        self.descripcion_entry.insert(0, budget.get("descripcion") or "")

        self.observaciones_entry.delete(0, "end")
        self.observaciones_entry.insert(0, budget.get("observaciones") or "")

        self.update_totals_labels(budget)

    def refresh_chapters(self):
        if not self.selected_id:
            self.chapters_table.clear()
            return

        chapters = self.controller.get_chapters(self.selected_id)

        chapters = self.format_chapters(chapters)

        self.chapters_table.load_data(chapters)

    def refresh_items(self):
        if not self.selected_capitulo_id:
            self.items_table.clear()
            return

        items = self.controller.get_items_by_chapter(
            self.selected_capitulo_id
        )

        items = self.format_items(items)

        self.items_table.load_data(items)

    def clear_all(self):
        self.selected_id = None
        self.selected_capitulo_id = None
        self.selected_item_id = None

        if self.project_options:
            self.project_option.set(self.project_options[0])

        if self.apu_options:
            self.apu_option.set(self.apu_options[0])

        self.codigo_entry.delete(0, "end")
        self.nombre_entry.delete(0, "end")
        self.fecha_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        self.observaciones_entry.delete(0, "end")

        self.clear_chapter_form()
        self.clear_item_form()

        self.chapters_table.clear()
        self.items_table.clear()

        self.update_totals_labels({
            "costo_directo_total": 0,
            "total_administracion": 0,
            "total_imprevistos": 0,
            "total_utilidad": 0,
            "valor_total_presupuesto": 0
        })

    def clear_chapter_form(self):
        self.selected_capitulo_id = None

        self.cap_codigo_entry.delete(0, "end")
        self.cap_nombre_entry.delete(0, "end")
        self.cap_orden_entry.delete(0, "end")
        self.cap_orden_entry.insert(0, "1")
        self.cap_descripcion_entry.delete(0, "end")

    def clear_item_form(self):
        self.selected_item_id = None

        if self.apu_options:
            self.apu_option.set(self.apu_options[0])

        self.item_codigo_entry.delete(0, "end")
        self.item_descripcion_entry.delete(0, "end")
        self.item_cantidad_entry.delete(0, "end")
        self.item_cantidad_entry.insert(0, "1")
        self.item_orden_entry.delete(0, "end")
        self.item_orden_entry.insert(0, "1")

    def update_totals_labels(self, budget):

        costo_directo = float(budget.get("costo_directo_total") or 0)
        administracion = float(budget.get("total_administracion") or 0)
        imprevistos = float(budget.get("total_imprevistos") or 0)
        utilidad = float(budget.get("total_utilidad") or 0)
        total = float(budget.get("valor_total_presupuesto") or 0)

        self.lbl_costo_directo.configure(
            text=f"Costo directo: {self.format_currency(costo_directo)}"
        )

        self.lbl_admin.configure(
            text=f"Administración: {self.format_currency(administracion)}"
        )

        self.lbl_imprevistos.configure(
            text=f"Imprevistos: {self.format_currency(imprevistos)}"
        )

        self.lbl_utilidad.configure(
            text=f"Utilidad: {self.format_currency(utilidad)}"
        )

        self.lbl_total.configure(
            text=f"Total: {self.format_currency(total)}"
        )