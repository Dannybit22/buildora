import customtkinter as ctk

from controllers.apu_controller import ApuController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class ApusView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = ApuController()
        self.selected_id = None

        self.units = []
        self.materials = []
        self.labor = []
        self.tools = []

        self.unit_options = []
        self.material_options = []
        self.labor_options = []
        self.tool_options = []

        self.load_catalogs()
        self.create_widgets()
        self.load_data()

    def load_catalogs(self):
        self.units = self.controller.get_active_units()
        self.materials = self.controller.get_active_materials()
        self.labor = self.controller.get_active_labor()
        self.tools = self.controller.get_active_tools()

        self.unit_map = {
            u["codigo_unidad"]: u["id_unidad"]
            for u in self.units
        }

        self.unit_options = sorted(
            list(self.unit_map.keys())
        )
        self.material_options = [f"{m['id_material']} - {m['codigo_material']} - {m['descripcion']}" for m in self.materials]
        self.labor_options = [f"{m['id_mano_obra']} - {m['codigo_mano_obra']} - {m['nombre_cargo']}" for m in self.labor]
        self.tool_options = [f"{h['id_herramienta']} - {h['codigo_herramienta']} - {h['nombre_herramienta']}" for h in self.tools]

        if not self.unit_options:
            self.unit_options = ["Sin unidades"]
        if not self.material_options:
            self.material_options = ["Sin materiales"]
        if not self.labor_options:
            self.labor_options = ["Sin mano de obra"]
        if not self.tool_options:
            self.tool_options = ["Sin herramientas"]

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Gestión de APUs", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(search_frame, width=360, placeholder_text="Buscar APU...")
        self.search_entry.pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="Buscar", command=self.search).pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Recargar", command=self.reload_all).pack(side="left", padx=5)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.create_label(form_frame, "Unidad", 0, 0)
        self.unit_option = ctk.CTkOptionMenu(form_frame, width=200, values=self.unit_options)
        self.unit_option.grid(row=0, column=1, padx=8, pady=6)

        self.create_label(form_frame, "Código APU", 0, 2)
        self.codigo_entry = ctk.CTkEntry(form_frame, width=220)
        self.codigo_entry.grid(row=0, column=3, padx=8, pady=6)

        self.create_label(form_frame, "Descripción", 1, 0)
        self.descripcion_entry = ctk.CTkEntry(form_frame, width=520)
        self.descripcion_entry.grid(row=1, column=1, columnspan=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Cantidad base", 2, 0)
        self.cantidad_entry = ctk.CTkEntry(form_frame, width=200)
        self.cantidad_entry.grid(row=2, column=1, padx=8, pady=6)
        self.cantidad_entry.insert(0, "1")

        self.create_label(form_frame, "Observaciones", 3, 0)
        self.observaciones_text = ctk.CTkTextbox(form_frame, width=520, height=60)
        self.observaciones_text.grid(row=3, column=1, columnspan=3, padx=8, pady=6, sticky="w")

        totals_frame = ctk.CTkFrame(self)
        totals_frame.pack(fill="x", padx=10, pady=5)

        self.lbl_materiales = self.create_total_label(totals_frame, "Materiales: $0", 0)
        self.lbl_mano_obra = self.create_total_label(totals_frame, "Mano de obra: $0", 1)
        self.lbl_herramientas = self.create_total_label(totals_frame, "Herramientas: $0", 2)
        self.lbl_total = self.create_total_label(totals_frame, "Costo directo total: $0", 3)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(button_frame, text="Guardar APU", command=self.save).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Actualizar APU", command=self.update).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Desactivar APU", command=self.disable).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

        apu_columns = [
            "id_apu", "codigo_apu", "descripcion", "codigo_unidad",
            "cantidad_base", "subtotal_materiales", "subtotal_mano_obra",
            "subtotal_herramientas", "costo_directo_total", "estado"
        ]

        apu_headings = {
            "id_apu": "ID",
            "codigo_apu": "Código",
            "descripcion": "Descripción",
            "codigo_unidad": "Und.",
            "cantidad_base": "Cant.",
            "subtotal_materiales": "Materiales",
            "subtotal_mano_obra": "Mano Obra",
            "subtotal_herramientas": "Herramientas",
            "costo_directo_total": "Total",
            "estado": "Estado"
        }

        self.apu_table = BaseTable(self, apu_columns, apu_headings)
        self.apu_table.pack(fill="x", padx=10, pady=4)
        self.apu_table.tree.bind("<<TreeviewSelect>>", self.on_select_apu)

        detail_frame = ctk.CTkFrame(self)
        detail_frame.pack(fill="x", padx=10, pady=5)

        self.create_detail_section(detail_frame)

    def create_detail_section(self, master):
        add_frame = ctk.CTkFrame(master)
        add_frame.pack(fill="x", padx=5, pady=5)

        self.material_option = ctk.CTkOptionMenu(add_frame, width=320, values=self.material_options)
        self.material_option.grid(row=0, column=0, padx=5, pady=5)
        self.material_qty = ctk.CTkEntry(add_frame, width=80, placeholder_text="Cant.")
        self.material_qty.grid(row=0, column=1, padx=5)
        ctk.CTkButton(add_frame, text="Agregar Material", command=self.add_material).grid(row=0, column=2, padx=5)

        self.labor_option = ctk.CTkOptionMenu(add_frame, width=320, values=self.labor_options)
        self.labor_option.grid(row=1, column=0, padx=5, pady=5)
        self.labor_qty = ctk.CTkEntry(add_frame, width=80, placeholder_text="Cant.")
        self.labor_qty.grid(row=1, column=1, padx=5)
        ctk.CTkButton(add_frame, text="Agregar Mano de Obra", command=self.add_labor).grid(row=1, column=2, padx=5)

        self.tool_option = ctk.CTkOptionMenu(add_frame, width=320, values=self.tool_options)
        self.tool_option.grid(row=2, column=0, padx=5, pady=5)
        self.tool_qty = ctk.CTkEntry(add_frame, width=80, placeholder_text="Cant.")
        self.tool_qty.grid(row=2, column=1, padx=5)
        ctk.CTkButton(add_frame, text="Agregar Herramienta", command=self.add_tool).grid(row=2, column=2, padx=5)

        tables_frame = ctk.CTkFrame(master)
        tables_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.materials_table = BaseTable(
            tables_frame,
            ["id_apu_material", "descripcion_material", "unidad_material", "cantidad", "valor_unitario", "subtotal"],
            {
                "id_apu_material": "ID",
                "descripcion_material": "Material",
                "unidad_material": "Unidad",
                "cantidad": "Cant.",
                "valor_unitario": "Valor Unit.",
                "subtotal": "Subtotal"
            }
        )
        self.materials_table.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.labor_table = BaseTable(
            tables_frame,
            ["id_apu_mano_obra", "nombre_cargo", "unidad_mano_obra", "cantidad", "valor_unitario", "subtotal"],
            {
                "id_apu_mano_obra": "ID",
                "nombre_cargo": "Cargo",
                "unidad_mano_obra": "Unidad",
                "cantidad": "Cant.",
                "valor_unitario": "Valor Unit.",
                "subtotal": "Subtotal"
            }
        )
        self.labor_table.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.tools_table = BaseTable(
            tables_frame,
            ["id_apu_herramienta", "nombre_herramienta", "unidad_herramienta", "cantidad", "valor_unitario", "subtotal"],
            {
                "id_apu_herramienta": "ID",
                "nombre_herramienta": "Herramienta",
                "unidad_herramienta": "Unidad",
                "cantidad": "Cant.",
                "valor_unitario": "Valor Unit.",
                "subtotal": "Subtotal"
            }
        )
        self.tools_table.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        tables_frame.grid_columnconfigure(0, weight=1)
        tables_frame.grid_columnconfigure(1, weight=1)
        tables_frame.grid_columnconfigure(2, weight=1)

        remove_frame = ctk.CTkFrame(master, fg_color="transparent")
        remove_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(remove_frame, text="Quitar Material", command=self.remove_material).pack(side="left", padx=5)
        ctk.CTkButton(remove_frame, text="Quitar Mano de Obra", command=self.remove_labor).pack(side="left", padx=5)
        ctk.CTkButton(remove_frame, text="Quitar Herramienta", command=self.remove_tool).pack(side="left", padx=5)

    def create_label(self, master, text, row, column):
        label = ctk.CTkLabel(master, text=text, font=("Arial", 12, "bold"))
        label.grid(row=row, column=column, padx=8, pady=6, sticky="w")

    def create_total_label(self, master, text, column):
        label = ctk.CTkLabel(master, text=text, font=("Arial", 13, "bold"))
        label.grid(row=0, column=column, padx=15, pady=8, sticky="w")
        return label

    def get_id_from_option(self, option_text, empty_text):
        if option_text == empty_text:
            return None
        try:
            return int(option_text.split(" - ")[0])
        except Exception:
            return None

    def get_selected_unit_id(self):
        selected = self.unit_option.get()

        if selected == "Sin unidades":
            return None

        return self.unit_map.get(selected)

    def find_by_id(self, records, key, record_id):
        for item in records:
            if item[key] == record_id:
                return item
        return None

    def get_form_data(self):
        return {
            "id_unidad": self.get_selected_unit_id(),
            "codigo_apu": self.codigo_entry.get().strip(),
            "descripcion": self.descripcion_entry.get().strip(),
            "cantidad_base": self.cantidad_entry.get().strip(),
            "observaciones": self.observaciones_text.get("1.0", "end").strip(),
            "estado": "activo"
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


    def format_apu_table(self, data):

        money_fields = [
            "subtotal_materiales",
            "subtotal_mano_obra",
            "subtotal_herramientas",
            "costo_directo_total"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data


    def format_detail_table(self, data):

        money_fields = [
            "valor_unitario",
            "subtotal"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data

    def load_data(self):
        data = self.controller.load_apus()
        data = self.format_apu_table(data)

        self.apu_table.load_data(data)
 
    def search(self):
        text = self.search_entry.get().strip()

        data = self.controller.search_apus(text)
        data = self.format_apu_table(data)

        self.apu_table.load_data(data)

    def reload_all(self):
        self.load_catalogs()
        self.unit_option.configure(values=self.unit_options)
        self.material_option.configure(values=self.material_options)
        self.labor_option.configure(values=self.labor_options)
        self.tool_option.configure(values=self.tool_options)

        self.clear()
        self.load_data()

    def save(self):
        try:
            apu_id = self.controller.create_apu(self.get_form_data())
            MessageUtils.success("APU creado correctamente.")
            self.clear()
            self.load_data()
            self.selected_id = apu_id
        except Exception as error:
            MessageUtils.error(str(error))

    def update(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un APU.")
            return

        try:
            self.controller.update_apu(self.selected_id, self.get_form_data())
            MessageUtils.success("APU actualizado correctamente.")
            self.load_data()
            self.refresh_details()
        except Exception as error:
            MessageUtils.error(str(error))

    def disable(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un APU.")
            return

        if not MessageUtils.confirm("¿Desea desactivar este APU?"):
            return

        self.controller.disable_apu(self.selected_id)
        MessageUtils.success("APU desactivado correctamente.")
        self.clear()
        self.load_data()

    def clear(self):
        self.selected_id = None

        if self.unit_options:
            self.unit_option.set(self.unit_options[0])
        if self.material_options:
            self.material_option.set(self.material_options[0])
        if self.labor_options:
            self.labor_option.set(self.labor_options[0])
        if self.tool_options:
            self.tool_option.set(self.tool_options[0])

        self.codigo_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, "1")
        self.observaciones_text.delete("1.0", "end")

        self.material_qty.delete(0, "end")
        self.labor_qty.delete(0, "end")
        self.tool_qty.delete(0, "end")

        self.materials_table.clear()
        self.labor_table.clear()
        self.tools_table.clear()

        self.update_totals_labels({
            "subtotal_materiales": 0,
            "subtotal_mano_obra": 0,
            "subtotal_herramientas": 0,
            "costo_directo_total": 0
        })

    def on_select_apu(self, event):
        values = self.apu_table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]
        apu = self.controller.get_apu(self.selected_id)

        if not apu:
            return

        for code, id_value in self.unit_map.items():
            if id_value == apu["id_unidad"]:
                self.unit_option.set(code)
                break

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, apu.get("codigo_apu") or "")

        self.descripcion_entry.delete(0, "end")
        self.descripcion_entry.insert(0, apu.get("descripcion") or "")

        self.cantidad_entry.delete(0, "end")
        self.cantidad_entry.insert(0, str(apu.get("cantidad_base") or "1"))

        self.observaciones_text.delete("1.0", "end")
        self.observaciones_text.insert("1.0", apu.get("observaciones") or "")

        self.update_totals_labels(apu)
        self.refresh_details()

    def refresh_details(self):
        if not self.selected_id:
            return

        materiales = self.controller.get_apu_materials(self.selected_id)
        materiales = self.format_detail_table(materiales)

        mano_obra = self.controller.get_apu_labor(self.selected_id)
        mano_obra = self.format_detail_table(mano_obra)

        herramientas = self.controller.get_apu_tools(self.selected_id)
        herramientas = self.format_detail_table(herramientas)

        self.materials_table.load_data(materiales)
        self.labor_table.load_data(mano_obra)
        self.tools_table.load_data(herramientas)

        apu = self.controller.get_apu(self.selected_id)
        if apu:
            self.update_totals_labels(apu)

    def add_material(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione o cree primero un APU.")
            return

        material_id = self.get_id_from_option(self.material_option.get(), "Sin materiales")
        material = self.find_by_id(self.materials, "id_material", material_id)

        try:
            self.controller.add_material(
                self.selected_id,
                material,
                self.material_qty.get()
            )
            MessageUtils.success("Material agregado al APU.")
            self.material_qty.delete(0, "end")
            self.refresh_details()
            self.load_data()
        except Exception as error:
            MessageUtils.error(str(error))

    def add_labor(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione o cree primero un APU.")
            return

        labor_id = self.get_id_from_option(self.labor_option.get(), "Sin mano de obra")
        labor = self.find_by_id(self.labor, "id_mano_obra", labor_id)

        try:
            self.controller.add_labor(
                self.selected_id,
                labor,
                self.labor_qty.get()
            )
            MessageUtils.success("Mano de obra agregada al APU.")
            self.labor_qty.delete(0, "end")
            self.refresh_details()
            self.load_data()
        except Exception as error:
            MessageUtils.error(str(error))

    def add_tool(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione o cree primero un APU.")
            return

        tool_id = self.get_id_from_option(self.tool_option.get(), "Sin herramientas")
        tool = self.find_by_id(self.tools, "id_herramienta", tool_id)

        try:
            self.controller.add_tool(
                self.selected_id,
                tool,
                self.tool_qty.get()
            )
            MessageUtils.success("Herramienta agregada al APU.")
            self.tool_qty.delete(0, "end")
            self.refresh_details()
            self.load_data()
        except Exception as error:
            MessageUtils.error(str(error))

    def remove_material(self):
        values = self.materials_table.get_selected_values()

        if not values:
            MessageUtils.warning("Seleccione un material del detalle.")
            return

        self.controller.remove_material(self.selected_id, values[0])
        self.refresh_details()
        self.load_data()

    def remove_labor(self):
        values = self.labor_table.get_selected_values()

        if not values:
            MessageUtils.warning("Seleccione una mano de obra del detalle.")
            return

        self.controller.remove_labor(self.selected_id, values[0])
        self.refresh_details()
        self.load_data()

    def remove_tool(self):
        values = self.tools_table.get_selected_values()

        if not values:
            MessageUtils.warning("Seleccione una herramienta del detalle.")
            return

        self.controller.remove_tool(self.selected_id, values[0])
        self.refresh_details()
        self.load_data()

    def update_totals_labels(self, apu):

        materiales = float(apu.get("subtotal_materiales") or 0)
        mano_obra = float(apu.get("subtotal_mano_obra") or 0)
        herramientas = float(apu.get("subtotal_herramientas") or 0)
        total = float(apu.get("costo_directo_total") or 0)

        self.lbl_materiales.configure(
            text=f"Materiales: {self.format_currency(materiales)}"
        )

        self.lbl_mano_obra.configure(
            text=f"Mano de obra: {self.format_currency(mano_obra)}"
        )

        self.lbl_herramientas.configure(
            text=f"Herramientas: {self.format_currency(herramientas)}"
        )

        self.lbl_total.configure(
            text=f"Costo directo total: {self.format_currency(total)}"
        )