from services.auth_service import AuthService


class AuthController:
    def __init__(self, login_view):
        self.login_view = login_view

    def login(self, username: str, password: str):
        result = AuthService.login(username, password)

        if result["success"]:
            self.login_view.open_main_layout(result["user"])
        else:
            self.login_view.show_error(result["message"])