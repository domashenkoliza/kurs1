from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class AddEmployeeModal(QDialog):
    def __init__(self, parent, on_submit_callback):
        super().__init__(parent)
        self.setWindowTitle("Добавить сотрудника")
        self.setGeometry(300, 300, 400, 500)

        self.layout = QVBoxLayout()

        # Поля ввода
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

        self.position_label = QLabel("Должность")
        self.layout.addWidget(self.position_label)
        self.position_input = QLineEdit()
        self.layout.addWidget(self.position_input)

        self.phone_label = QLabel("Телефон")
        self.layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_input)

        self.login_label = QLabel("Логин")
        self.layout.addWidget(self.login_label)
        self.login_input = QLineEdit()
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel("Пароль")
        self.layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

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
        data = {
            "surname": self.surname_input.text(),
            "name": self.name_input.text(),
            "patronymic": self.patronymic_input.text(),
            "position": self.position_input.text(),
            "phone": self.phone_input.text(),
            "login": self.login_input.text(),
            "password": self.password_input.text(),
        }

        if not all(data.values()):
            QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
            return

        self.on_submit_callback(data)
        self.accept()
