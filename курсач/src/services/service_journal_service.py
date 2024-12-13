from sqlalchemy.orm import Session

from src.database.models import ServiceJournal


class ServiceJournalService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add_service(self, name: str, cost: float):
        service = ServiceJournal(name=name, cost=cost)
        self._db_session.add(service)
        self._db_session.commit()
        return service

    def get_services(self):
        return self._db_session.query(ServiceJournal).all()

    def delete_service(self, service_id: int):
        service = self._db_session.query(ServiceJournal).get(service_id)
        if service:
            self._db_session.delete(service)
            self._db_session.commit()
