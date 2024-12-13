from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QAbstractItemView,
)
from gui.modals.add_repair_modal import AddRepairModal
from services.repair_service import RepairService
from database.models import Client, Shoe, Employee


class RepairsTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

        self.layout = QVBoxLayout()

        # Таблица ремонтов
        self.repairs_table = QTableWidget()
        self.repairs_table.setColumnCount(7)
        self.repairs_table.setHorizontalHeaderLabels(
            ["ID", "ID Обуви", "ID Клиента", "ID Сотрудника", "Статус", "Дата приёма", "Срок ремонта"]
        )

        # Запрещаем мультивыбор
        self.repairs_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Выделение строк
        self.repairs_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # Только одна строка

        self.layout.addWidget(self.repairs_table)

        # Кнопки управления
        self.add_repair_button = QPushButton("Добавить ремонт")
        self.add_repair_button.clicked.connect(self.open_add_repair_modal)
        self.layout.addWidget(self.add_repair_button)

        self.delete_repair_button = QPushButton("Удалить ремонт")
        self.delete_repair_button.clicked.connect(self.delete_repair)
        self.layout.addWidget(self.delete_repair_button)

        self.setLayout(self.layout)
        self.refresh_repairs_list()

    def refresh_repairs_list(self):
        """Обновляет таблицу ремонтов."""
        with self.session_factory() as session:
            repair_service = RepairService(session)
            repairs = repair_service.get_repairs()

        self.repairs_table.setRowCount(len(repairs))
        for row, repair in enumerate(repairs):
            self.repairs_table.setItem(row, 0, QTableWidgetItem(str(repair.id)))
            self.repairs_table.setItem(row, 1, QTableWidgetItem(str(repair.shoe_id)))
            self.repairs_table.setItem(row, 2, QTableWidgetItem(str(repair.client_id)))
            self.repairs_table.setItem(row, 3, QTableWidgetItem(str(repair.employee_id)))
            self.repairs_table.setItem(row, 4, QTableWidgetItem(repair.status))
            self.repairs_table.setItem(row, 5, QTableWidgetItem(str(repair.received_date)))
            self.repairs_table.setItem(row, 6, QTableWidgetItem(str(repair.due_date)))

    def refresh(self):
        """Refresh the repairs table."""
        self.refresh_repairs_list()

    def open_add_repair_modal(self):
        """Открывает модальное окно для добавления ремонта."""

        def on_submit(data):
            if not all(data.values()):
                QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
                return

            with self.session_factory() as session:
                repair_service = RepairService(session)
                repair_service.create_repair(
                    data["shoe_id"],
                    data["client_id"],
                    data["employee_id"],
                    data["status"],
                    data["received_date"],
                    data["due_date"],
                )

            self.refresh_repairs_list()
            QMessageBox.information(self, "Успех", "Ремонт добавлен!")

        # Получение данных для выпадающих списков
        with self.session_factory() as session:
            clients = [{"id": c.id, "name": f"{c.surname} {c.name}"} for c in session.query(Client).all()]
            shoes = [{"id": s.id, "name": s.name} for s in session.query(Shoe).all()]
            employees = [{"id": e.id, "name": f"{e.surname} {e.name}"} for e in session.query(Employee).all()]

        modal = AddRepairModal(self, on_submit, clients, shoes, employees)
        modal.exec()

    def delete_repair(self):
        """Удаляет выбранный ремонт."""
        selected_row = self.repairs_table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Ошибка", "Выберите ремонт для удаления!")
            return

        repair_id = int(self.repairs_table.item(selected_row, 0).text())

        with self.session_factory() as session:
            repair_service = RepairService(session)
            repair_service.delete_repair(repair_id)

        self.refresh_repairs_list()
        QMessageBox.information(self, "Успех", "Ремонт удален!")
