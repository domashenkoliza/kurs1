from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class AddRepairModal(QDialog):
    def __init__(self, parent, on_submit_callback, clients, shoes, employees):
        super().__init__(parent)
        self.setWindowTitle("Добавить ремонт")
        self.setGeometry(300, 300, 400, 450)

        self.layout = QVBoxLayout()

        # Список обуви
        self.shoe_label = QLabel("Обувь")
        self.layout.addWidget(self.shoe_label)
        self.shoe_combobox = QComboBox()
        self.shoe_combobox.addItems([f"{shoe['id']}: {shoe['name']}" for shoe in shoes])
        self.layout.addWidget(self.shoe_combobox)

        # Список клиентов
        self.client_label = QLabel("Клиент")
        self.layout.addWidget(self.client_label)
        self.client_combobox = QComboBox()
        self.client_combobox.addItems([f"{client['id']}: {client['name']}" for client in clients])
        self.layout.addWidget(self.client_combobox)

        # Список сотрудников
        self.employee_label = QLabel("Сотрудник")
        self.layout.addWidget(self.employee_label)
        self.employee_combobox = QComboBox()
        self.employee_combobox.addItems([f"{employee['id']}: {employee['name']}" for employee in employees])
        self.layout.addWidget(self.employee_combobox)

        # Статус ремонта
        self.status_label = QLabel("Статус")
        self.layout.addWidget(self.status_label)
        self.status_input = QLineEdit()
        self.layout.addWidget(self.status_input)

        # Дата приёма
        self.received_date_label = QLabel("Дата приёма (YYYY-MM-DD)")
        self.layout.addWidget(self.received_date_label)
        self.received_date_input = QLineEdit()
        self.layout.addWidget(self.received_date_input)

        # Срок ремонта
        self.due_date_label = QLabel("Срок ремонта (YYYY-MM-DD)")
        self.layout.addWidget(self.due_date_label)
        self.due_date_input = QLineEdit()
        self.layout.addWidget(self.due_date_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Добавить")
        self.submit_button.clicked.connect(self.submit)
        button_layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

        self.on_submit_callback = on_submit_callback

    def submit(self):
        """Отправка данных из формы."""
        try:
            # Получаем выбранные ID из выпадающих списков
            shoe_id = int(self.shoe_combobox.currentText().split(":")[0])
            client_id = int(self.client_combobox.currentText().split(":")[0])
            employee_id = int(self.employee_combobox.currentText().split(":")[0])

            data = {
                "shoe_id": shoe_id,
                "client_id": client_id,
                "employee_id": employee_id,
                "status": self.status_input.text(),
                "received_date": self.received_date_input.text(),
                "due_date": self.due_date_input.text(),
            }

            self.on_submit_callback(data)
            self.accept()

        except (ValueError, IndexError):
            QMessageBox.critical(
                self,
                "Ошибка",
                "Пожалуйста, выберите корректные данные или заполните поля правильно!"
            )
