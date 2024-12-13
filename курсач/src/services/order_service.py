from sqlalchemy.orm import Session

from src.database.models import Order


class OrderService:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def create_order(self, repair_id: int, employee_id: int, client_id: int, total_cost: float, order_date):
        order = Order(
            repair_id=repair_id,
            employee_id=employee_id,
            client_id=client_id,
            total_cost=total_cost,
            order_date=order_date
        )
        self._db_session.add(order)
        self._db_session.commit()
        return order

    def get_orders(self):
        return self._db_session.query(Order).all()

    def get_order_details(self, order_id: int):
        return self._db_session.query(Order).filter_by(id=order_id).first()

    def delete_order(self, order_id: int):
        """Удаляет заказ по его ID."""
        order = self._db_session.query(Order).filter_by(id=order_id).first()
        if not order:
            raise ValueError(f"Заказ с ID {order_id} не найден")
        self._db_session.delete(order)
        self._db_session.commit()
