from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView
)
from gui.modals.add_client_modal import AddClientModal
from services.user_service import UserService


class ClientsTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

        self.layout = QVBoxLayout()

        # Таблица клиентов
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Телефон"])
        self.clients_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # Запрет на мультивыбор
        self.layout.addWidget(self.clients_table)

        # Кнопки
        self.add_client_button = QPushButton("Добавить клиента")
        self.add_client_button.clicked.connect(self.open_add_client_modal)
        self.layout.addWidget(self.add_client_button)

        self.delete_client_button = QPushButton("Удалить клиента")
        self.delete_client_button.clicked.connect(self.delete_client)
        self.layout.addWidget(self.delete_client_button)

        self.setLayout(self.layout)
        self.refresh_clients_list()

    def refresh_clients_list(self):
        """Обновляет список клиентов в таблице."""
        with self.session_factory() as session:
            user_service = UserService(session)
            clients = user_service.get_clients()

        self.clients_table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            self.clients_table.setItem(row, 0, QTableWidgetItem(str(client.id)))
            self.clients_table.setItem(row, 1, QTableWidgetItem(client.surname))
            self.clients_table.setItem(row, 2, QTableWidgetItem(client.name))
            self.clients_table.setItem(row, 3, QTableWidgetItem(client.patronymic))
            self.clients_table.setItem(row, 4, QTableWidgetItem(client.phone))
            
    def refresh(self):
        """Refresh the clients table."""
        self.refresh_clients_list()

    def open_add_client_modal(self):
        """Открывает модальное окно для добавления клиента."""
        def on_submit(data):
            with self.session_factory() as session:
                user_service = UserService(session)
                user_service.add_client(data["surname"], data["name"], data["patronymic"], data["phone"])

            self.refresh_clients_list()

        modal = AddClientModal(self, on_submit)
        modal.exec()

    def delete_client(self):
        """Удаляет выбранного клиента."""
        selected_row = self.clients_table.currentRow()
        if selected_row == -1:
            return

        client_id = int(self.clients_table.item(selected_row, 0).text())

        with self.session_factory() as session:
            user_service = UserService(session)
            user_service.delete_client(client_id)

        self.refresh_clients_list()
