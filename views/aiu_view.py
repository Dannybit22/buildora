import customtkinter as ctk

from controllers.aiu_controller import AiuController
from utils.message_utils import MessageUtils


class AiuView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.controller = AiuController()
        self.selected_budget_id = None

        self.budgets = []
        self.budget_options = []

        self.load_budgets()
        self.create_widgets()

    def load_budgets(self):
        self.budgets = self.controller.get_active_budgets()

        self.budget_options = [
            f"{b['id_presupuesto']} - {b['codigo_presupuesto']} - {b['nombre_presupuesto']}"
            for b in self.budgets
        ]

        if not self.budget_options:
            self.budget_options = ["Sin presupuestos activos"]

    def create_widgets(self):
        title = ctk.CTkLabel(
            self,
            text="AIU - Administración, Imprevistos y Utilidad",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        selector_frame = ctk.CTkFrame(self)
        selector_frame.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            selector_frame,
            text="Presupuesto",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=8, pady=6, sticky="w")

        self.budget_option = ctk.CTkOptionMenu(
            selector_frame,
            width=520,
            values=self.budget_options
        )
        self.budget_option.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        ctk.CTkButton(
            selector_frame,
            text="Cargar",
            command=self.load_selected_budget
        ).grid(row=0, column=2, padx=8, pady=6)

        ctk.CTkButton(
            selector_frame,
            text="Recargar",
            command=self.reload_budgets
        ).grid(row=0, column=3, padx=8, pady=6)

        totals_frame = ctk.CTkFrame(self)
        totals_frame.pack(fill="x", padx=10, pady=8)

        self.lbl_directo = self.total_label(totals_frame, "Costo directo: $0", 0)
        self.lbl_admin = self.total_label(totals_frame, "Administración: $0", 1)
        self.lbl_imp = self.total_label(totals_frame, "Imprevistos: $0", 2)
        self.lbl_util = self.total_label(totals_frame, "Utilidad: $0", 3)
        self.lbl_iva = self.total_label(totals_frame, "IVA utilidad: $0", 4)
        self.lbl_total = self.total_label(totals_frame, "Total presupuesto: $0", 5)

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=10, pady=8)

        self.create_admin_section(body)
        self.create_imprevistos_section(body)
        self.create_utilidad_section(body)

    def total_label(self, master, text, column):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=("Arial", 12, "bold")
        )
        label.grid(row=0, column=column, padx=10, pady=8, sticky="w")
        return label

    def create_label(self, master, text, row, column):
        label = ctk.CTkLabel(
            master,
            text=text,
            font=("Arial", 11, "bold")
        )
        label.grid(row=row, column=column, padx=6, pady=4, sticky="w")

    def create_entry(self, master, row, column):
        entry = ctk.CTkEntry(master, width=150)
        entry.grid(row=row, column=column, padx=6, pady=4, sticky="w")
        entry.insert(0, "0")
        return entry

    def create_admin_section(self, master):
        frame = ctk.CTkFrame(master)
        frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Administración",
            font=("Arial", 17, "bold")
        ).grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="w")

        self.create_label(frame, "Personal técnico", 1, 0)
        self.admin_tecnico = self.create_entry(frame, 1, 1)

        self.create_label(frame, "Personal administrativo", 2, 0)
        self.admin_administrativo = self.create_entry(frame, 2, 1)

        self.create_label(frame, "Ocupacional", 3, 0)
        self.admin_ocupacional = self.create_entry(frame, 3, 1)

        self.create_label(frame, "Dotación oficina", 4, 0)
        self.admin_dotacion = self.create_entry(frame, 4, 1)

        self.create_label(frame, "Equipos", 5, 0)
        self.admin_equipos = self.create_entry(frame, 5, 1)

        self.create_label(frame, "Caja menor", 6, 0)
        self.admin_caja = self.create_entry(frame, 6, 1)

        self.create_label(frame, "Garantías", 7, 0)
        self.admin_garantias = self.create_entry(frame, 7, 1)

        self.create_label(frame, "Impuestos", 8, 0)
        self.admin_impuestos = self.create_entry(frame, 8, 1)

        self.create_label(frame, "Observaciones", 9, 0)
        self.admin_obs = ctk.CTkTextbox(frame, width=300, height=60)
        self.admin_obs.grid(row=9, column=1, padx=6, pady=4)

        ctk.CTkButton(
            frame,
            text="Guardar Administración",
            command=self.save_admin
        ).grid(row=10, column=0, columnspan=2, padx=8, pady=10)

    def create_imprevistos_section(self, master):
        frame = ctk.CTkFrame(master)
        frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Imprevistos",
            font=("Arial", 17, "bold")
        ).grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="w")

        self.create_label(frame, "Mano de obra", 1, 0)
        self.imp_mano_obra = self.create_entry(frame, 1, 1)

        self.create_label(frame, "Materiales", 2, 0)
        self.imp_materiales = self.create_entry(frame, 2, 1)

        self.create_label(frame, "Riesgo", 3, 0)
        self.imp_riesgo = self.create_entry(frame, 3, 1)

        self.create_label(frame, "Administración", 4, 0)
        self.imp_administracion = self.create_entry(frame, 4, 1)

        self.create_label(frame, "Observaciones", 5, 0)
        self.imp_obs = ctk.CTkTextbox(frame, width=300, height=60)
        self.imp_obs.grid(row=5, column=1, padx=6, pady=4)

        ctk.CTkButton(
            frame,
            text="Guardar Imprevistos",
            command=self.save_imprevistos
        ).grid(row=6, column=0, columnspan=2, padx=8, pady=10)

    def create_utilidad_section(self, master):
        frame = ctk.CTkFrame(master)
        frame.grid(row=0, column=2, padx=8, pady=8, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text="Utilidad",
            font=("Arial", 17, "bold")
        ).grid(row=0, column=0, columnspan=4, padx=8, pady=8, sticky="w")

        self.create_label(frame, "% Utilidad operativa", 1, 0)
        self.util_porcentaje = self.create_entry(frame, 1, 1)

        self.create_label(frame, "% Retefuente", 2, 0)
        self.util_retefuente = self.create_entry(frame, 2, 1)

        self.create_label(frame, "% Renta", 3, 0)
        self.util_renta = self.create_entry(frame, 3, 1)

        self.create_label(frame, "% IVA utilidad", 4, 0)
        self.util_iva = self.create_entry(frame, 4, 1)

        self.create_label(frame, "Observaciones", 5, 0)
        self.util_obs = ctk.CTkTextbox(frame, width=300, height=60)
        self.util_obs.grid(row=5, column=1, padx=6, pady=4)

        ctk.CTkButton(
            frame,
            text="Guardar Utilidad",
            command=self.save_utilidad
        ).grid(row=6, column=0, columnspan=2, padx=8, pady=10)

        ctk.CTkButton(
            frame,
            text="Calcular AIU",
            command=self.calculate_aiu
        ).grid(row=7, column=0, columnspan=2, padx=8, pady=10)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def get_selected_budget_id(self):
        selected = self.budget_option.get()

        if selected == "Sin presupuestos activos":
            return None

        try:
            return int(selected.split(" - ")[0])
        except Exception:
            return None

    def reload_budgets(self):
        self.load_budgets()
        self.budget_option.configure(values=self.budget_options)

        if self.budget_options:
            self.budget_option.set(self.budget_options[0])

        self.selected_budget_id = None
        self.clear_forms()
        self.update_totals({})

    def load_selected_budget(self):
        self.selected_budget_id = self.get_selected_budget_id()

        if not self.selected_budget_id:
            MessageUtils.warning("Seleccione un presupuesto.")
            return

        budget = self.controller.get_budget(self.selected_budget_id)

        if not budget:
            MessageUtils.error("No se encontró el presupuesto.")
            return

        self.load_existing_data()
        self.update_totals(budget)

    def load_existing_data(self):
        admin = self.controller.get_administracion(self.selected_budget_id)
        imp = self.controller.get_imprevistos(self.selected_budget_id)
        util = self.controller.get_utilidad(self.selected_budget_id)

        self.clear_forms()

        if admin:
            self.set_entry(self.admin_tecnico, admin.get("total_personal_tecnico"))
            self.set_entry(self.admin_administrativo, admin.get("total_personal_administrativo"))
            self.set_entry(self.admin_ocupacional, admin.get("total_ocupacional"))
            self.set_entry(self.admin_dotacion, admin.get("total_dotacion_oficina"))
            self.set_entry(self.admin_equipos, admin.get("total_equipos"))
            self.set_entry(self.admin_caja, admin.get("total_caja_menor"))
            self.set_entry(self.admin_garantias, admin.get("total_garantias"))
            self.set_entry(self.admin_impuestos, admin.get("total_impuestos"))
            self.set_text(self.admin_obs, admin.get("observaciones"))

        if imp:
            self.set_entry(self.imp_mano_obra, imp.get("total_imprevisto_mano_obra"))
            self.set_entry(self.imp_materiales, imp.get("total_imprevisto_materiales"))
            self.set_entry(self.imp_riesgo, imp.get("total_imprevisto_riesgo"))
            self.set_entry(self.imp_administracion, imp.get("total_imprevisto_administracion"))
            self.set_text(self.imp_obs, imp.get("observaciones"))

        if util:
            self.set_entry(self.util_porcentaje, util.get("porcentaje_utilidad_operativa"))
            self.set_entry(self.util_retefuente, util.get("porcentaje_retefuente"))
            self.set_entry(self.util_renta, util.get("porcentaje_renta"))
            self.set_entry(self.util_iva, util.get("porcentaje_iva_utilidad"))
            self.set_text(self.util_obs, util.get("observaciones"))

    def save_admin(self):
        if not self.selected_budget_id:
            MessageUtils.warning("Cargue primero un presupuesto.")
            return

        try:
            self.controller.save_administracion(
                self.selected_budget_id,
                {
                    "total_personal_tecnico": self.admin_tecnico.get(),
                    "total_personal_administrativo": self.admin_administrativo.get(),
                    "total_ocupacional": self.admin_ocupacional.get(),
                    "total_dotacion_oficina": self.admin_dotacion.get(),
                    "total_equipos": self.admin_equipos.get(),
                    "total_caja_menor": self.admin_caja.get(),
                    "total_garantias": self.admin_garantias.get(),
                    "total_impuestos": self.admin_impuestos.get(),
                    "observaciones": self.admin_obs.get("1.0", "end").strip()
                }
            )

            MessageUtils.success("Administración guardada correctamente.")
            self.refresh_totals()

        except Exception as error:
            MessageUtils.error(str(error))

    def save_imprevistos(self):
        if not self.selected_budget_id:
            MessageUtils.warning("Cargue primero un presupuesto.")
            return

        try:
            self.controller.save_imprevistos(
                self.selected_budget_id,
                {
                    "total_imprevisto_mano_obra": self.imp_mano_obra.get(),
                    "total_imprevisto_materiales": self.imp_materiales.get(),
                    "total_imprevisto_riesgo": self.imp_riesgo.get(),
                    "total_imprevisto_administracion": self.imp_administracion.get(),
                    "observaciones": self.imp_obs.get("1.0", "end").strip()
                }
            )

            MessageUtils.success("Imprevistos guardados correctamente.")
            self.refresh_totals()

        except Exception as error:
            MessageUtils.error(str(error))

    def save_utilidad(self):
        if not self.selected_budget_id:
            MessageUtils.warning("Cargue primero un presupuesto.")
            return

        try:
            self.controller.save_utilidad(
                self.selected_budget_id,
                {
                    "porcentaje_utilidad_operativa": self.util_porcentaje.get(),
                    "porcentaje_retefuente": self.util_retefuente.get(),
                    "porcentaje_renta": self.util_renta.get(),
                    "porcentaje_iva_utilidad": self.util_iva.get(),
                    "observaciones": self.util_obs.get("1.0", "end").strip()
                }
            )

            MessageUtils.success("Utilidad guardada correctamente.")
            self.refresh_totals()

        except Exception as error:
            MessageUtils.error(str(error))

    def calculate_aiu(self):
        if not self.selected_budget_id:
            MessageUtils.warning("Cargue primero un presupuesto.")
            return

        try:
            aiu = self.controller.recalculate_aiu(self.selected_budget_id)
            MessageUtils.success("AIU calculado correctamente.")
            self.update_totals(aiu)

        except Exception as error:
            MessageUtils.error(str(error))

    def refresh_totals(self):
        budget = self.controller.get_budget(self.selected_budget_id)
        if budget:
            self.update_totals(budget)

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

    def update_totals(self, data):
        costo_directo = float(data.get("costo_directo_total") or 0)
        admin = float(data.get("total_administracion") or 0)
        imp = float(data.get("total_imprevistos") or 0)
        util = float(data.get("total_utilidad") or 0)
        iva = float(data.get("iva_utilidad") or 0)
        total = float(data.get("valor_total_presupuesto") or 0)

        self.lbl_directo.configure(
            text=f"Costo directo: {self.format_currency(costo_directo)}"
        )
        self.lbl_admin.configure(
            text=f"Administración: {self.format_currency(admin)}"
        )
        self.lbl_imp.configure(
            text=f"Imprevistos: {self.format_currency(imp)}"
        )
        self.lbl_util.configure(
            text=f"Utilidad: {self.format_currency(util)}"
        )
        self.lbl_iva.configure(
            text=f"IVA utilidad: {self.format_currency(iva)}"
        )
        self.lbl_total.configure(
            text=f"Total presupuesto: {self.format_currency(total)}"
        )

    def set_entry(self, entry, value):
        entry.delete(0, "end")
        entry.insert(0, str(value or 0))

    def set_text(self, textbox, value):
        textbox.delete("1.0", "end")
        textbox.insert("1.0", value or "")

    def clear_forms(self):
        entries = [
            self.admin_tecnico,
            self.admin_administrativo,
            self.admin_ocupacional,
            self.admin_dotacion,
            self.admin_equipos,
            self.admin_caja,
            self.admin_garantias,
            self.admin_impuestos,
            self.imp_mano_obra,
            self.imp_materiales,
            self.imp_riesgo,
            self.imp_administracion,
            self.util_porcentaje,
            self.util_retefuente,
            self.util_renta,
            self.util_iva
        ]

        for entry in entries:
            self.set_entry(entry, 0)

        for textbox in [
            self.admin_obs,
            self.imp_obs,
            self.util_obs
        ]:
            textbox.delete("1.0", "end")