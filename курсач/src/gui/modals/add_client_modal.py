from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton


class AddClientModal(QDialog):
    def __init__(self, parent, on_submit_callback):
        super().__init__(parent)
        self.setWindowTitle("Добавить клиента")
        self.setGeometry(300, 300, 400, 300)

        self.layout = QVBoxLayout()

        self.surname_label = QLabel("Фамилия")
        self.layout.addWidget(self.surname_label)

        self.surname_input = QLineEdit()
        self.layout.addWidget(self.surname_input)

        self.name_label = QLabel("Имя")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.patronymic_label = QLabel("Отчество")
        self.layout.addWidget(self.patronymic_label)

        self.patronymic_input = QLineEdit()
        self.layout.addWidget(self.patronymic_input)

        self.phone_label = QLabel("Телефон")
        self.layout.addWidget(self.phone_label)

        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_input)

        self.submit_button = QPushButton("Добавить")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.on_submit_callback = on_submit_callback
        self.setLayout(self.layout)

    def submit(self):
        """Handles the submit action."""
        data = {
            "surname": self.surname_input.text(),
            "name": self.name_input.text(),
            "patronymic": self.patronymic_input.text(),
            "phone": self.phone_input.text(),
        }

        if not all(data.values()):
            QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
            return

        self.on_submit_callback(data)
        self.accept()
