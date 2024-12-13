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


class AddOrderModal(QDialog):
    def __init__(self, parent, on_submit_callback, repairs, employees, clients):
        super().__init__(parent)
        self.setWindowTitle("Добавить заказ")
        self.setGeometry(300, 300, 400, 450)

        self.layout = QVBoxLayout()

        # Список ремонтов
        self.repair_label = QLabel("Ремонт")
        self.layout.addWidget(self.repair_label)
        self.repair_combobox = QComboBox()
        self.repair_combobox.addItems([f"{repair['id']}: {repair['description']}" for repair in repairs])
        self.layout.addWidget(self.repair_combobox)

        # Список сотрудников
        self.employee_label = QLabel("Сотрудник")
        self.layout.addWidget(self.employee_label)
        self.employee_combobox = QComboBox()
        self.employee_combobox.addItems([f"{employee['id']}: {employee['name']}" for employee in employees])
        self.layout.addWidget(self.employee_combobox)

        # Список клиентов
        self.client_label = QLabel("Клиент")
        self.layout.addWidget(self.client_label)
        self.client_combobox = QComboBox()
        self.client_combobox.addItems([f"{client['id']}: {client['name']}" for client in clients])
        self.layout.addWidget(self.client_combobox)

        # Общая стоимость
        self.total_cost_label = QLabel("Общая стоимость")
        self.layout.addWidget(self.total_cost_label)
        self.total_cost_input = QLineEdit()
        self.layout.addWidget(self.total_cost_input)

        # Дата заказа
        self.order_date_label = QLabel("Дата заказа (YYYY-MM-DD)")
        self.layout.addWidget(self.order_date_label)
        self.order_date_input = QLineEdit()
        self.layout.addWidget(self.order_date_input)

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
            repair_id = int(self.repair_combobox.currentText().split(":")[0])
            employee_id = int(self.employee_combobox.currentText().split(":")[0])
            client_id = int(self.client_combobox.currentText().split(":")[0])

            data = {
                "repair_id": repair_id,
                "employee_id": employee_id,
                "client_id": client_id,
                "total_cost": float(self.total_cost_input.text()),
                "order_date": self.order_date_input.text(),
            }

            self.on_submit_callback(data)
            self.accept()

        except (ValueError, IndexError):
            QMessageBox.critical(
                self,
                "Ошибка",
                "Пожалуйста, выберите корректные данные или заполните поля правильно!"
            )
