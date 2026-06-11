import customtkinter as ctk
from config.app_config import COLOR_PANEL, COLOR_TEXT, COLOR_MUTED_TEXT


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color=COLOR_PANEL)

        self.user = user

        title = ctk.CTkLabel(
            self,
            text="Dashboard Buildora",
            font=("Arial", 26, "bold"),
            text_color=COLOR_TEXT
        )
        title.pack(pady=(40, 10))

        subtitle = ctk.CTkLabel(
            self,
            text=f"Bienvenido, {user['nombres']} {user['apellidos']} | Rol: {user['nombre_rol']}",
            font=("Arial", 14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(pady=10)

        info = ctk.CTkLabel(
            self,
            text="Sistema de gestión de presupuestos de obra basado en APUs.",
            font=("Arial", 14),
            text_color=COLOR_TEXT
        )
        info.pack(pady=20)