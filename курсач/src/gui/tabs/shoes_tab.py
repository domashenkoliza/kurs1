from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QAbstractItemView,
)
from gui.modals.add_shoe_modal import AddShoeModal
from services.shoe_service import ShoeService
from database.models import Client, ServiceJournal


class ShoesTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory
        self.setWindowTitle("Список обуви")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        # Таблица обуви
        self.shoes_table = QTableWidget()
        self.shoes_table.setColumnCount(5)
        self.shoes_table.setHorizontalHeaderLabels(["ID", "ID Услуги", "ID Клиента", "Размер", "Наименование"])
        self.shoes_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # Только одна строка
        self.layout.addWidget(self.shoes_table)

        # Кнопки управления
        self.add_shoe_button = QPushButton("Добавить обувь")
        self.add_shoe_button.clicked.connect(self.open_add_shoe_modal)
        self.layout.addWidget(self.add_shoe_button)

        self.delete_shoe_button = QPushButton("Удалить обувь")
        self.delete_shoe_button.clicked.connect(self.delete_shoe)
        self.layout.addWidget(self.delete_shoe_button)

        self.setLayout(self.layout)
        self.refresh_shoes_list()

    def refresh_shoes_list(self):
        """Обновляет таблицу обуви."""
        try:
            with self.session_factory() as session:
                shoe_service = ShoeService(session)
                shoes = shoe_service.get_shoes()

            self.shoes_table.setRowCount(len(shoes))
            for row, shoe in enumerate(shoes):
                self.shoes_table.setItem(row, 0, QTableWidgetItem(str(shoe.id)))
                self.shoes_table.setItem(row, 1, QTableWidgetItem(str(shoe.service_id)))
                self.shoes_table.setItem(row, 2, QTableWidgetItem(str(shoe.client_id)))
                self.shoes_table.setItem(row, 3, QTableWidgetItem(shoe.size))
                self.shoes_table.setItem(row, 4, QTableWidgetItem(shoe.name))
        except Exception as e:
            self.show_error_dialog(f"Ошибка при обновлении списка обуви: {e}")

    def refresh(self):
        """Refresh the shoes table."""
        self.refresh_shoes_list()

    def open_add_shoe_modal(self):
        """Открывает модальное окно для добавления обуви."""

        def on_submit(data):
            try:
                if not all(data.values()):
                    raise ValueError("Заполните все поля!")

                with self.session_factory() as session:
                    shoe_service = ShoeService(session)
                    shoe_service.add_shoe(data["service_id"], data["client_id"], data["size"], data["name"])

                self.refresh_shoes_list()
                QMessageBox.information(self, "Успех", "Обувь добавлена!")
            except Exception as e:
                self.show_error_dialog(f"Ошибка при добавлении обуви: {e}")

        try:
            with self.session_factory() as session:
                clients = [{"id": c.id, "name": f"{c.surname} {c.name}"} for c in session.query(Client).all()]
                services = [{"id": s.id, "name": s.name} for s in session.query(ServiceJournal).all()]

            modal = AddShoeModal(self, on_submit, clients, services)
            modal.exec()
        except Exception as e:
            self.show_error_dialog(f"Ошибка при открытии модального окна: {e}")

    def delete_shoe(self):
        """Удаляет выбранную обувь."""
        try:
            selected_row = self.shoes_table.currentRow()
            if selected_row == -1:
                raise ValueError("Выберите обувь для удаления!")

            shoe_id = int(self.shoes_table.item(selected_row, 0).text())

            with self.session_factory() as session:
                shoe_service = ShoeService(session)
                shoe_service.delete_shoe(shoe_id)

            self.refresh_shoes_list()
            QMessageBox.information(self, "Успех", "Обувь удалена!")
        except Exception as e:
            self.show_error_dialog(f"Ошибка при удалении обуви: {e}")

    def show_error_dialog(self, message):
        """Показывает диалоговое окно с ошибкой."""
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.exec()
