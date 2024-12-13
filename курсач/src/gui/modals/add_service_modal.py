from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)


class AddServiceModal(QDialog):
    def __init__(self, parent, on_submit_callback):
        super().__init__(parent)
        self.setWindowTitle("Добавить услугу")
        self.setGeometry(300, 300, 300, 200)

        self.layout = QVBoxLayout()

        # Наименование услуги
        self.name_label = QLabel("Наименование услуги")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        # Стоимость услуги
        self.cost_label = QLabel("Стоимость")
        self.layout.addWidget(self.cost_label)
        self.cost_input = QLineEdit()
        self.layout.addWidget(self.cost_input)

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
        data = {
            "name": self.name_input.text(),
            "cost": self.cost_input.text(),
        }

        if not data["name"] or not data["cost"]:
            QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
            return

        # Validate cost is a float
        try:
            data["cost"] = float(data["cost"])
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Стоимость должна быть числом!")
            return

        self.on_submit_callback(data)
        self.accept()
