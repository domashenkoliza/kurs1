import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.services.auth_service import AuthService
from src.services.employee_service import EmployeeService
from src.services.order_service import OrderService
from src.services.repair_service import RepairService
from src.services.service_journal_service import ServiceJournalService
from src.services.shoe_service import ShoeService
from src.services.user_service import UserService

DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db_session():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_service(test_db_session):
    return AuthService(test_db_session)

@pytest.fixture
def employee_service(test_db_session):
    return EmployeeService(test_db_session)

@pytest.fixture
def order_service(test_db_session):
    return OrderService(test_db_session)

@pytest.fixture
def repair_service(test_db_session):
    return RepairService(test_db_session)

@pytest.fixture
def service_journal_service(test_db_session):
    return ServiceJournalService(test_db_session)

@pytest.fixture
def shoe_service(test_db_session):
    return ShoeService(test_db_session)

@pytest.fixture
def user_service(test_db_session):
    return UserService(test_db_session)
