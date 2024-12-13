from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QAbstractItemView,
)
from gui.modals.add_order_modal import AddOrderModal
from services.order_service import OrderService
from database.models import Client, Employee, Repair


class OrdersTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

        self.layout = QVBoxLayout()

        # Таблица заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels(
            ["ID", "ID Ремонта", "ID Сотрудника", "ID Клиента", "Стоимость", "Дата заказа"]
        )

        # Запрещаем мультивыбор
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Выделение целых строк
        self.orders_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # Только одна строка

        self.layout.addWidget(self.orders_table)

        # Кнопки управления
        self.add_order_button = QPushButton("Добавить заказ")
        self.add_order_button.clicked.connect(self.open_add_order_modal)
        self.layout.addWidget(self.add_order_button)

        self.delete_order_button = QPushButton("Удалить заказ")
        self.delete_order_button.clicked.connect(self.delete_order)
        self.layout.addWidget(self.delete_order_button)

        self.setLayout(self.layout)
        self.refresh_orders_list()

    def refresh_orders_list(self):
        """Обновляет таблицу заказов."""
        with self.session_factory() as session:
            order_service = OrderService(session)
            orders = order_service.get_orders()

        self.orders_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(order.repair_id)))
            self.orders_table.setItem(row, 2, QTableWidgetItem(str(order.employee_id)))
            self.orders_table.setItem(row, 3, QTableWidgetItem(str(order.client_id)))
            self.orders_table.setItem(row, 4, QTableWidgetItem(f"{order.total_cost:.2f}"))
            self.orders_table.setItem(row, 5, QTableWidgetItem(str(order.order_date)))

    def refresh(self):
        """Refresh the orders table."""
        self.refresh_orders_list()

    def open_add_order_modal(self):
        """Открывает модальное окно для добавления заказа."""

        def on_submit(data):
            if not all(data.values()):
                QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
                return

            with self.session_factory() as session:
                order_service = OrderService(session)
                order_service.create_order(
                    data["repair_id"],
                    data["employee_id"],
                    data["client_id"],
                    data["total_cost"],
                    data["order_date"],
                )

            self.refresh_orders_list()
            QMessageBox.information(self, "Успех", "Заказ добавлен!")

        # Получение данных для выпадающих списков
        with self.session_factory() as session:
            repairs = [{"id": r.id, "description": f"Ремонт обуви ID {r.shoe_id}"} for r in session.query(Repair).all()]
            employees = [{"id": e.id, "name": f"{e.surname} {e.name}"} for e in session.query(Employee).all()]
            clients = [{"id": c.id, "name": f"{c.surname} {c.name}"} for c in session.query(Client).all()]

        modal = AddOrderModal(self, on_submit, repairs, employees, clients)
        modal.exec()

    def delete_order(self):
        """Удаляет выбранный заказ."""
        selected_row = self.orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Ошибка", "Выберите заказ для удаления!")
            return

        order_id = int(self.orders_table.item(selected_row, 0).text())

        with self.session_factory() as session:
            order_service = OrderService(session)
            order_service.delete_order(order_id)

        self.refresh_orders_list()
        QMessageBox.information(self, "Успех", "Заказ удален!")
