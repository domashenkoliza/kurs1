from sqlalchemy.orm import Session

from src.database.models import Shoe


class ShoeService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add_shoe(self, service_id: int, client_id: int, size: str, name: str):
        shoe = Shoe(service_id=service_id, client_id=client_id, size=size, name=name)
        self._db_session.add(shoe)
        self._db_session.commit()
        return shoe

    def get_shoes(self):
        return self._db_session.query(Shoe).all()

    def delete_shoe(self, shoe_id: int):
        shoe = self._db_session.query(Shoe).get(shoe_id)
        if shoe:
            self._db_session.delete(shoe)
            self._db_session.commit()
