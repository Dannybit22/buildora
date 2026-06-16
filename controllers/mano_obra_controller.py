from services.mano_obra_service import ManoObraService


class ManoObraController:

    def __init__(self):
        self.service = ManoObraService()

    def load_records(self):
        return self.service.get_all()

    def search_records(self, text):
        return self.service.search(text)

    def get_record(self, record_id):
        return self.service.get_by_id(record_id)

    def create_record(self, data):
        return self.service.create(data)

    def update_record(self, record_id, data):
        return self.service.update(record_id, data)

    def disable_record(self, record_id):
        return self.service.disable(record_id)