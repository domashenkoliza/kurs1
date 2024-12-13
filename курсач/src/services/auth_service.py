from sqlalchemy.orm import Session

from src.database.models import Employee


class AuthService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def authenticate(self, login: str, password: str):
        """
        Проверяет учетные данные пользователя.
        """
        user = self._db_session.query(Employee).filter_by(login=login).first()
        if user and user.password == password:
            return user
        return None
