import customtkinter as ctk
from config.app_config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_PRIMARY,
    COLOR_TEXT
)
from views.dashboard_view import DashboardView
from views.clientes_view import ClientesView 

class MainLayout(ctk.CTkToplevel):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(1000, 650)
        self.configure(fg_color=COLOR_BACKGROUND)

        self.sidebar = ctk.CTkFrame(self, width=220, fg_color="#181818")
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, fg_color=COLOR_PANEL)
        self.content.pack(side="right", expand=True, fill="both")

        self.create_sidebar()
        self.show_dashboard()

    def create_sidebar(self):
        logo = ctk.CTkLabel(
            self.sidebar,
            text="BUILDORA",
            font=("Arial", 24, "bold"),
            text_color=COLOR_PRIMARY
        )
        logo.pack(pady=(30, 20))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Clientes", self.show_clients),
            ("Proyectos", self.not_available),
            ("Materiales", self.not_available),
            ("Mano de obra", self.not_available),
            ("Herramientas", self.not_available),
            ("APUs", self.not_available),
            ("Presupuestos", self.not_available),
            ("AIU", self.not_available),
            ("Reportes", self.not_available),
            ("Parámetros", self.not_available),
            ("Salir", self.exit_app),
        ]

        for text, command in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color="#333333",
                text_color=COLOR_TEXT,
                anchor="w"
            )
            button.pack(fill="x", padx=15, pady=5)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()
        dashboard = DashboardView(self.content, self.user)
        dashboard.pack(expand=True, fill="both")

    def not_available(self):
        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Módulo en construcción",
            font=("Arial", 24, "bold"),
            text_color=COLOR_TEXT
        )
        label.pack(expand=True)

    def exit_app(self):
        self.destroy()

    def show_clients(self):

        self.clear_content()

        frame = ClientesView(self.content)

        frame.pack(
            expand=True,
            fill="both"
        )