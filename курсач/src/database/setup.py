import os
import random

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Employee, Client, ServiceJournal, Shoe, Repair, Order


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")#"postgresql+psycopg2://postgres:postgres@localhost:15432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
fake = Faker()


def generate_synthetic_data(session):
    # Добавление сотрудников
    positions = ["Мастер", "Администратор", "Кассир"]
    for i in range(10):
        try:
            employee = Employee(
                surname=fake.last_name(),
                name=fake.first_name(),
                patronymic=f"{fake.first_name()}вич",  # Сгенерированное отчество
                position=random.choice(positions),
                phone=fake.phone_number(),
                login=f"user{i}",
                password="password"  # Хеширование пароля для реального проекта
            )
            session.add(employee)
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")

    # Добавление клиентов
    for i in range(20):
        try:
            client = Client(
                surname=fake.last_name(),
                name=fake.first_name(),
                patronymic=f"{fake.first_name()}вна",  # Сгенерированное отчество
                phone=fake.phone_number()
            )
            session.add(client)
        except Exception as e:
            print(f"Ошибка при добавлении клиента: {e}")

    # Добавление услуг
    services = [
        {"name": "Ремонт подошвы", "cost": 1000.0},
        {"name": "Замена каблуков", "cost": 500.0},
        {"name": "Чистка обуви", "cost": 300.0},
        {"name": "Ремонт молнии", "cost": 700.0},
    ]
    for service in services:
        try:
            service_journal = ServiceJournal(name=service["name"], cost=service["cost"])
            session.add(service_journal)
        except Exception as e:
            print(f"Ошибка при добавлении услуги: {e}")

    session.commit()  # Фиксируем данные, чтобы использовать их для связей

    # Добавление обуви
    service_ids = [service.id for service in session.query(ServiceJournal).all()]
    client_ids = [client.id for client in session.query(Client).all()]

    for i in range(30):
        try:
            shoe = Shoe(
                service_id=random.choice(service_ids),
                client_id=random.choice(client_ids),
                size=str(random.randint(35, 45)),
                name=fake.word() + " обувь"
            )
            session.add(shoe)
        except Exception as e:
            print(f"Ошибка при добавлении обуви: {e}")

    session.commit()

    # Добавление ремонтов
    shoe_ids = [shoe.id for shoe in session.query(Shoe).all()]
    employee_ids = [employee.id for employee in session.query(Employee).all()]

    for i in range(15):
        try:
            repair = Repair(
                shoe_id=random.choice(shoe_ids),
                client_id=random.choice(client_ids),
                employee_id=random.choice(employee_ids),
                status=random.choice(["Ожидание", "В процессе", "Завершено"]),
                received_date=fake.date_this_year(),
                due_date=fake.date_this_year()
            )
            session.add(repair)
        except Exception as e:
            print(f"Ошибка при добавлении ремонта: {e}")

    session.commit()

    # Добавление заказов
    repair_ids = [repair.id for repair in session.query(Repair).all()]

    for i in range(20):
        try:
            order = Order(
                repair_id=random.choice(repair_ids),
                employee_id=random.choice(employee_ids),
                client_id=random.choice(client_ids),
                total_cost=round(random.uniform(500, 5000), 2),
                order_date=fake.date_this_year()
            )
            session.add(order)
        except Exception as e:
            print(f"Ошибка при добавлении заказа: {e}")

    session.commit()
    print("Синтетические данные успешно добавлены!")


def init_db():
    Base.metadata.create_all(bind=engine)

    # Создаем тестового сотрудника
    with SessionLocal() as session:
        if not session.query(Employee).filter_by(login="admin").first():
            admin = Employee(
                surname="Админ",
                name="Иван",
                patronymic="Иванович",
                position="Администратор",
                phone="1234567890",
                login="admin",
                password="password"  # Для реального проекта используйте хеширование
            )
            session.add(admin)
            session.commit()
            
        # Генерация синтетических данных
        try:
            generate_synthetic_data(session)
        except Exception:
            pass
