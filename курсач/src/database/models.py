from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    phone = Column(String, nullable=False)

    # Связь с заказами
    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")
    # Связь с обувью
    shoes = relationship("Shoe", back_populates="client", cascade="all, delete-orphan")
    # Связь с ремонтами
    repairs = relationship("Repair", back_populates="client", cascade="all, delete-orphan")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    position = Column(String, nullable=False)  # Должность
    phone = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Связь с заказами
    orders = relationship("Order", back_populates="employee", cascade="all, delete-orphan")
    # Связь с ремонтами
    repairs = relationship("Repair", back_populates="employee", cascade="all, delete-orphan")


class ServiceJournal(Base):
    __tablename__ = "service_journal"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Наименование услуги
    cost = Column(Float, nullable=False)  # Стоимость услуги

    # Связь с обувью
    shoes = relationship("Shoe", back_populates="service", cascade="all, delete-orphan")


class Shoe(Base):
    __tablename__ = "shoes"
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("service_journal.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    size = Column(String, nullable=False)  # Размер обуви
    name = Column(String, nullable=False)  # Наименование обуви

    # Связи
    service = relationship("ServiceJournal", back_populates="shoes")
    client = relationship("Client", back_populates="shoes")
    repairs = relationship("Repair", back_populates="shoe", cascade="all, delete-orphan")


class Repair(Base):
    __tablename__ = "repairs"
    id = Column(Integer, primary_key=True, index=True)
    shoe_id = Column(Integer, ForeignKey("shoes.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    status = Column(String, nullable=False)  # Статус заказа
    received_date = Column(Date, nullable=False)  # Дата приёма
    due_date = Column(Date, nullable=False)  # Срок ремонта

    # Связи
    shoe = relationship("Shoe", back_populates="repairs")
    client = relationship("Client", back_populates="repairs")
    employee = relationship("Employee", back_populates="repairs")
    orders = relationship("Order", back_populates="repair", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    repair_id = Column(Integer, ForeignKey("repairs.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    total_cost = Column(Float, nullable=False)  # Общая стоимость
    order_date = Column(Date, nullable=False)  # Дата заказа

    # Связи
    client = relationship("Client", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    repair = relationship("Repair", back_populates="orders")