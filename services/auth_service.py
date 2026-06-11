from repositories.usuario_repository import UsuarioRepository
from utils.security import Security


class AuthService:
    @staticmethod
    def login(username: str, password: str):
        if not username or not password:
            return {
                "success": False,
                "message": "Debe ingresar usuario y contraseña.",
                "user": None
            }

        user = UsuarioRepository.find_by_username(username)

        if not user:
            return {
                "success": False,
                "message": "Usuario no encontrado.",
                "user": None
            }

        if user["estado"] != "activo":
            return {
                "success": False,
                "message": "El usuario se encuentra inactivo.",
                "user": None
            }

        is_valid = Security.verify_password(password, user["password_hash"])

        if not is_valid:
            return {
                "success": False,
                "message": "Contraseña incorrecta.",
                "user": None
            }

        UsuarioRepository.update_last_access(user["id_usuario"])

        return {
            "success": True,
            "message": "Inicio de sesión exitoso.",
            "user": user
        }