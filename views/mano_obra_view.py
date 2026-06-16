import customtkinter as ctk

from controllers.mano_obra_controller import ManoObraController
from views.components.base_table import BaseTable
from utils.message_utils import MessageUtils


class ManoObraView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = ManoObraController()
        self.selected_id = None

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="Gestión de Mano de Obra",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=5)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=360,
            placeholder_text="Buscar por código, cargo o contratación..."
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

        self.create_label(form_frame, "Código", 0, 0)
        self.codigo_entry = ctk.CTkEntry(form_frame, width=240)
        self.codigo_entry.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Cargo", 0, 2)
        self.cargo_entry = ctk.CTkEntry(form_frame, width=300)
        self.cargo_entry.grid(row=0, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "SMMLV", 1, 0)
        self.smmlv_entry = ctk.CTkEntry(form_frame, width=240)
        self.smmlv_entry.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Tipo contratación", 1, 2)
        self.tipo_option = ctk.CTkOptionMenu(
            form_frame,
            width=240,
            values=[
                "Contrato completo",
                "Prestación de servicios"
            ]
        )
        self.tipo_option.grid(row=1, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Dedicación", 2, 0)
        self.dedicacion_entry = ctk.CTkEntry(form_frame, width=240)
        self.dedicacion_entry.grid(row=2, column=1, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "Días proyectados", 2, 2)
        self.dias_entry = ctk.CTkEntry(form_frame, width=240)
        self.dias_entry.grid(row=2, column=3, padx=8, pady=6, sticky="w")

        self.create_label(form_frame, "N° trabajadores", 3, 0)
        self.trabajadores_entry = ctk.CTkEntry(form_frame, width=240)
        self.trabajadores_entry.grid(row=3, column=1, padx=8, pady=6, sticky="w")

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
            "id_mano_obra",
            "codigo_mano_obra",
            "nombre_cargo",
            "cantidad_smmlv",
            "tipo_contratacion",
            "salario_base",
            "total_contratacion",
            "costo_dia",
            "valor_total",
            "estado"
        ]

        headings = {
            "id_mano_obra": "ID",
            "codigo_mano_obra": "Código",
            "nombre_cargo": "Cargo",
            "cantidad_smmlv": "SMMLV",
            "tipo_contratacion": "Contratación",
            "salario_base": "Salario Base",
            "total_contratacion": "Total Contrato",
            "costo_dia": "Costo Día",
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

    def get_tipo_db(self):
        tipo = self.tipo_option.get()

        if tipo == "Prestación de servicios":
            return "prestacion_servicios"

        return "contrato_completo"

    def set_tipo_from_db(self, value):
        if value == "prestacion_servicios":
            self.tipo_option.set("Prestación de servicios")
        else:
            self.tipo_option.set("Contrato completo")

    def get_form_data(self):
        return {
            "codigo_mano_obra": self.codigo_entry.get().strip(),
            "nombre_cargo": self.cargo_entry.get().strip(),
            "cantidad_smmlv": self.smmlv_entry.get().strip(),
            "tipo_contratacion": self.get_tipo_db(),
            "dedicacion": self.dedicacion_entry.get().strip(),
            "dias_proyectados": self.dias_entry.get().strip(),
            "numero_trabajadores": self.trabajadores_entry.get().strip(),
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


    def format_money_fields(self, data):
        money_fields = [
            "salario_base",
            "total_contratacion",
            "costo_dia",
            "valor_total"
        ]

        for item in data:
            for field in money_fields:
                if field in item:
                    item[field] = self.format_currency(item[field])

        return data


    def load_data(self):
        data = self.controller.load_records()
        data = self.format_money_fields(data)
        self.table.load_data(data)


    def search(self):
        text = self.search_entry.get().strip()

        if not text:
            self.load_data()
            return

        data = self.controller.search_records(text)
        data = self.format_money_fields(data)
        self.table.load_data(data)

    def reload_all(self):
        self.search_entry.delete(0, "end")
        self.clear()
        self.load_data()

    def save(self):
        try:
            data = self.get_form_data()
            self.controller.create_record(data)

            MessageUtils.success("Registro de mano de obra creado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def update(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un registro.")
            return

        try:
            data = self.get_form_data()
            self.controller.update_record(self.selected_id, data)

            MessageUtils.success("Registro actualizado correctamente.")

            self.clear()
            self.load_data()

        except Exception as error:
            MessageUtils.error(str(error))

    def disable(self):
        if not self.selected_id:
            MessageUtils.warning("Seleccione un registro.")
            return

        confirm = MessageUtils.confirm(
            "¿Desea desactivar este registro de mano de obra?"
        )

        if not confirm:
            return

        self.controller.disable_record(self.selected_id)

        MessageUtils.success("Registro desactivado correctamente.")

        self.clear()
        self.load_data()

    def clear(self):
        self.selected_id = None

        self.codigo_entry.delete(0, "end")
        self.cargo_entry.delete(0, "end")
        self.smmlv_entry.delete(0, "end")
        self.dedicacion_entry.delete(0, "end")
        self.dias_entry.delete(0, "end")
        self.trabajadores_entry.delete(0, "end")

        self.smmlv_entry.insert(0, "1")
        self.dedicacion_entry.insert(0, "1")
        self.dias_entry.insert(0, "0")
        self.trabajadores_entry.insert(0, "1")
        self.tipo_option.set("Contrato completo")

    def on_select(self, event):
        values = self.table.get_selected_values()

        if not values:
            return

        self.selected_id = values[0]
        record = self.controller.get_record(self.selected_id)

        if not record:
            return

        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, record.get("codigo_mano_obra") or "")

        self.cargo_entry.delete(0, "end")
        self.cargo_entry.insert(0, record.get("nombre_cargo") or "")

        self.smmlv_entry.delete(0, "end")
        self.smmlv_entry.insert(0, str(record.get("cantidad_smmlv") or "1"))

        self.set_tipo_from_db(record.get("tipo_contratacion"))

        self.dedicacion_entry.delete(0, "end")
        self.dedicacion_entry.insert(0, str(record.get("dedicacion") or "1"))

        self.dias_entry.delete(0, "end")
        self.dias_entry.insert(0, str(record.get("dias_proyectados") or "0"))

        self.trabajadores_entry.delete(0, "end")
        self.trabajadores_entry.insert(0, str(record.get("numero_trabajadores") or "1"))