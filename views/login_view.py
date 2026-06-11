import customtkinter as ctk
from tkinter import messagebox

from config.app_config import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BACKGROUND,
    COLOR_PANEL,
    COLOR_PRIMARY,
    COLOR_TEXT,
    COLOR_MUTED_TEXT
)
from controllers.auth_controller import AuthController
from views.main_layout import MainLayout


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controller = AuthController(self)

        self.title(f"{APP_NAME} - Login")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(900, 600)
        self.configure(fg_color=COLOR_BACKGROUND)

        self.create_widgets()

    def create_widgets(self):
        container = ctk.CTkFrame(
            self,
            width=420,
            height=470,
            fg_color=COLOR_PANEL,
            corner_radius=18
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            container,
            text="BUILDORA",
            font=("Arial", 34, "bold"),
            text_color=COLOR_PRIMARY
        )
        title.pack(pady=(45, 5))

        subtitle = ctk.CTkLabel(
            container,
            text="Gestión de presupuestos de obra",
            font=("Arial", 14),
            text_color=COLOR_MUTED_TEXT
        )
        subtitle.pack(pady=(0, 35))

        self.username_entry = ctk.CTkEntry(
            container,
            width=300,
            height=42,
            placeholder_text="Usuario"
        )
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(
            container,
            width=300,
            height=42,
            placeholder_text="Contraseña",
            show="*"
        )
        self.password_entry.pack(pady=10)

        login_button = ctk.CTkButton(
            container,
            width=300,
            height=42,
            text="Iniciar sesión",
            fg_color=COLOR_PRIMARY,
            hover_color="#D9AD18",
            text_color="#000000",
            font=("Arial", 14, "bold"),
            command=self.handle_login
        )
        login_button.pack(pady=(25, 10))

        footer = ctk.CTkLabel(
            container,
            text="Versión 1.0.0",
            font=("Arial", 11),
            text_color=COLOR_MUTED_TEXT
        )
        footer.pack(pady=(25, 0))

        self.bind("<Return>", lambda event: self.handle_login())

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        self.controller.login(username, password)

    def show_error(self, message: str):
        messagebox.showerror("Error de autenticación", message)

    def open_main_layout(self, user):
        main_window = MainLayout(user)
        main_window.grab_set()
        self.withdraw()