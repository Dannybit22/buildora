from tkinter import messagebox


class MessageUtils:
    @staticmethod
    def info(message: str):
        messagebox.showinfo("Información", message)

    @staticmethod
    def success(message: str):
        messagebox.showinfo("Operación exitosa", message)

    @staticmethod
    def warning(message: str):
        messagebox.showwarning("Advertencia", message)

    @staticmethod
    def error(message: str):
        messagebox.showerror("Error", message)

    @staticmethod
    def confirm(message: str) -> bool:
        return messagebox.askyesno("Confirmar", message)