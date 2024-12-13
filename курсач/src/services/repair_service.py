from sqlalchemy.orm import Session

from src.database.models import Repair


class RepairService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def create_repair(self, shoe_id: int, client_id: int, employee_id: int, status: str, received_date, due_date):
        repair = Repair(
            shoe_id=shoe_id,
            client_id=client_id,
            employee_id=employee_id,
            status=status,
            received_date=received_date,
            due_date=due_date
        )
        self._db_session.add(repair)
        self._db_session.commit()
        return repair

    def get_repairs(self):
        return self._db_session.query(Repair).all()

    def delete_repair(self, repair_id: int):
        """Удаляет ремонт по его ID."""
        repair = self._db_session.query(Repair).filter_by(id=repair_id).first()
        if not repair:
            raise ValueError(f"Ремонт с ID {repair_id} не найден")
        self._db_session.delete(repair)
        self._db_session.commit()
