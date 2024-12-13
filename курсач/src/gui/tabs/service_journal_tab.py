from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QAbstractItemView,
)
from gui.modals.add_service_modal import AddServiceModal
from services.service_journal_service import ServiceJournalService


class ServiceJournalTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

        self.layout = QVBoxLayout()

        # Таблица услуг
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(3)
        self.services_table.setHorizontalHeaderLabels(["ID", "Наименование", "Стоимость"])

        # Запрет мультивыбора
        self.services_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Выделение строк
        self.services_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # Только одна строка

        self.layout.addWidget(self.services_table)

        # Кнопки управления
        self.add_service_button = QPushButton("Добавить услугу")
        self.add_service_button.clicked.connect(self.open_add_service_modal)
        self.layout.addWidget(self.add_service_button)

        self.delete_service_button = QPushButton("Удалить услугу")
        self.delete_service_button.clicked.connect(self.delete_service)
        self.layout.addWidget(self.delete_service_button)

        self.setLayout(self.layout)
        self.refresh_service_list()

    def refresh_service_list(self):
        """Обновляет таблицу услуг."""
        with self.session_factory() as session:
            service_journal_service = ServiceJournalService(session)
            services = service_journal_service.get_services()

        self.services_table.setRowCount(len(services))
        for row, service in enumerate(services):
            self.services_table.setItem(row, 0, QTableWidgetItem(str(service.id)))
            self.services_table.setItem(row, 1, QTableWidgetItem(service.name))
            self.services_table.setItem(row, 2, QTableWidgetItem(f"{service.cost:.2f}"))

    def refresh(self):
        """Refresh the services table."""
        self.refresh_service_list()

    def open_add_service_modal(self):
        """Открывает модальное окно для добавления услуги."""

        def on_submit(data):
            if not all(data.values()):
                QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
                return

            try:
                data["cost"] = float(data["cost"])
            except ValueError:
                QMessageBox.critical(self, "Ошибка", "Стоимость должна быть числом!")
                return

            with self.session_factory() as session:
                service_journal_service = ServiceJournalService(session)
                service_journal_service.add_service(data["name"], data["cost"])

            self.refresh_service_list()
            QMessageBox.information(self, "Успех", "Услуга добавлена!")

        modal = AddServiceModal(self, on_submit)
        modal.exec()

    def delete_service(self):
        """Удаляет выбранную услугу."""
        selected_row = self.services_table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Ошибка", "Выберите услугу для удаления!")
            return

        service_id = int(self.services_table.item(selected_row, 0).text())

        with self.session_factory() as session:
            service_journal_service = ServiceJournalService(session)
            service_journal_service.delete_service(service_id)

        self.refresh_service_list()
        QMessageBox.information(self, "Успех", "Услуга удалена!")
