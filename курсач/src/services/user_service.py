from sqlalchemy.orm import Session

from src.database.models import Client


class UserService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add_client(self, surname: str, name: str, patronymic: str, phone: str):
        client = Client(surname=surname, name=name, patronymic=patronymic, phone=phone)
        self._db_session.add(client)
        self._db_session.commit()
        return client

    def get_clients(self):
        return self._db_session.query(Client).all()

    def find_client(self, phone: str):
        return self._db_session.query(Client).filter_by(phone=phone).first()

    def delete_client(self, client_id: int):
        client = self._db_session.query(Client).get(client_id)
        if client:
            self._db_session.delete(client)
            self._db_session.commit()
