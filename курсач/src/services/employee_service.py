from sqlalchemy.orm import Session

from src.database.models import Employee


class EmployeeService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def add_employee(self, surname: str, name: str, patronymic: str, position: str, phone: str, login: str, password: str):
        employee = Employee(
            surname=surname,
            name=name,
            patronymic=patronymic,
            position=position,
            phone=phone,
            login=login,
            password=password
        )
        self._db_session.add(employee)
        self._db_session.commit()
        return employee

    def get_employees(self):
        return self._db_session.query(Employee).all()

    def delete_employee(self, employee_id: int):
        """Удаляет сотрудника по его ID."""
        employee = self._db_session.query(Employee).filter_by(id=employee_id).first()
        if not employee:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден")
        self._db_session.delete(employee)
        self._db_session.commit()
