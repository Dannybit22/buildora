import customtkinter as ctk
from database.connection import DatabaseConnection
from views.login_view import LoginView


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    if not DatabaseConnection.test_connection():
        print("No fue posible conectar con la base de datos Buildora.")
        return

    app = LoginView()
    app.mainloop()


if __name__ == "__main__":
    main()