from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class AddShoeModal(QDialog):
    def __init__(self, parent, on_submit_callback, clients, services):
        super().__init__(parent)
        self.setWindowTitle("Добавить обувь")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()

        # Выбор услуги
        self.service_label = QLabel("Услуга")
        self.layout.addWidget(self.service_label)
        self.service_combobox = QComboBox()
        self.service_combobox.addItems([f"{service['id']}: {service['name']}" for service in services])
        self.layout.addWidget(self.service_combobox)

        # Выбор клиента
        self.client_label = QLabel("Клиент")
        self.layout.addWidget(self.client_label)
        self.client_combobox = QComboBox()
        self.client_combobox.addItems([f"{client['id']}: {client['name']}" for client in clients])
        self.layout.addWidget(self.client_combobox)

        # Размер обуви
        self.size_label = QLabel("Размер")
        self.layout.addWidget(self.size_label)
        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_input)

        # Наименование обуви
        self.name_label = QLabel("Наименование")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

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
            service_id = int(self.service_combobox.currentText().split(":")[0])
            client_id = int(self.client_combobox.currentText().split(":")[0])

            data = {
                "service_id": service_id,
                "client_id": client_id,
                "size": self.size_input.text(),
                "name": self.name_input.text(),
            }

            if not all(data.values()):
                QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
                return

            self.on_submit_callback(data)
            self.accept()
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Выберите корректные значения из выпадающих списков!")
