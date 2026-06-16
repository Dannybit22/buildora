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
from views.proyectos_view import ProyectosView
from views.materiales_view import MaterialesView
from views.mano_obra_view import ManoObraView    
from views.herramientas_view import HerramientasView
from views.apus_view import ApusView    
from views.presupuestos_view import PresupuestosView        
from views.aiu_view import AiuView
from views.reportes_view import ReportesView
import os
from PIL import Image
from utils.resource_path import resource_path


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
        logo_path = resource_path(
            os.path.join("assets", "buildora_logo.jpg")
        )

        img = Image.open(logo_path)

        logo_image = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(165, 55)
        )

        logo = ctk.CTkLabel(
            self.sidebar,
            image=logo_image,
            text=""
        )
        logo.image = logo_image
        logo.pack(pady=(30, 20))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Clientes", self.show_clients),
            ("Proyectos", self.show_projects),
            ("Materiales", self.show_materials),
            ("Mano de obra", self.show_mano_obra),
            ("Herramientas", self.show_herramientas),
            ("APUs", self.show_apus),
            ("Presupuestos", self.show_presupuestos),
            ("AIU", self.show_aiu),
            ("Reportes", self.show_reportes),
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
        
    def show_projects(self):
        self.clear_content()

        frame = ProyectosView(self.content)
        frame.pack(expand=True, fill="both")
        
    def show_materials(self):
        self.clear_content()

        frame = MaterialesView(self.content)
        frame.pack(expand=True, fill="both")
        
    def show_mano_obra(self):
        self.clear_content()

        frame = ManoObraView(self.content)
        frame.pack(expand=True, fill="both")

    def show_herramientas(self):

        self.clear_content()

        frame = HerramientasView(
            self.content
        )

        frame.pack(
            fill="both",
            expand=True
        )
        
    def show_apus(self):
        self.clear_content()

        frame = ApusView(self.content)
        frame.pack(expand=True, fill="both")
        
    def show_presupuestos(self):
        self.clear_content()

        frame = PresupuestosView(self.content, self.user)
        frame.pack(expand=True, fill="both")
        
    def show_aiu(self):
        self.clear_content()

        frame = AiuView(self.content)
        frame.pack(expand=True, fill="both")
        
    def show_reportes(self):
        self.clear_content()

        frame = ReportesView(self.content)
        frame.pack(expand=True, fill="both")