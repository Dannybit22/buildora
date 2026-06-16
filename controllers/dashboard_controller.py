from services.dashboard_service import DashboardService


class DashboardController:

    def __init__(self):
        self.service = DashboardService()

    def get_summary(self):
        return self.service.get_summary()