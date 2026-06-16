from repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self):
        self.repository = DashboardRepository()

    def get_summary(self):
        return {
            "clientes": self.repository.count_table("clientes"),
            "proyectos": self.repository.count_table("proyectos"),
            "materiales": self.repository.count_table("materiales"),
            "mano_obra": self.repository.count_table("mano_obra"),
            "herramientas": self.repository.count_table("herramientas"),
            "apus": self.repository.count_table("apus"),
            "presupuestos": self.repository.count_presupuestos(),
            "costo_directo": self.repository.total_costo_directo(),
            "valor_presupuestado": self.repository.total_valor_presupuestado(),
            "ultimos_presupuestos": self.repository.get_latest_budgets()
        }