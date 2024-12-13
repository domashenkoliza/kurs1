from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
    QAbstractItemView,
)
from gui.modals.add_employee_modal import AddEmployeeModal
from services.employee_service import EmployeeService


class EmployeesTab(QWidget):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory

        self.layout = QVBoxLayout()

        # Таблица сотрудников
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(7)
        self.employees_table.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Должность", "Телефон", "Логин"]
        )
        self.employees_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.employees_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layout.addWidget(self.employees_table)

        # Кнопки управления
        self.add_employee_button = QPushButton("Добавить сотрудника")
        self.add_employee_button.clicked.connect(self.open_add_employee_modal)
        self.layout.addWidget(self.add_employee_button)

        self.delete_employee_button = QPushButton("Удалить сотрудника")
        self.delete_employee_button.clicked.connect(self.delete_employee)
        self.layout.addWidget(self.delete_employee_button)

        self.setLayout(self.layout)
        self.refresh_employees_list()

    def refresh_employees_list(self):
        """Обновляет таблицу сотрудников."""
        with self.session_factory() as session:
            employee_service = EmployeeService(session)
            employees = employee_service.get_employees()

        self.employees_table.setRowCount(len(employees))
        for row, employee in enumerate(employees):
            self.employees_table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            self.employees_table.setItem(row, 1, QTableWidgetItem(employee.surname))
            self.employees_table.setItem(row, 2, QTableWidgetItem(employee.name))
            self.employees_table.setItem(row, 3, QTableWidgetItem(employee.patronymic))
            self.employees_table.setItem(row, 4, QTableWidgetItem(employee.position))
            self.employees_table.setItem(row, 5, QTableWidgetItem(employee.phone))
            self.employees_table.setItem(row, 6, QTableWidgetItem(employee.login))
            
    def refresh(self):
        """Refresh the employees table."""
        self.refresh_employees_list()

    def open_add_employee_modal(self):
        """Открывает модальное окно для добавления сотрудника."""

        def on_submit(data):
            if not all(data.values()):
                QMessageBox.critical(self, "Ошибка", "Заполните все поля!")
                return

            with self.session_factory() as session:
                employee_service = EmployeeService(session)
                employee_service.add_employee(
                    data["surname"],
                    data["name"],
                    data["patronymic"],
                    data["position"],
                    data["phone"],
                    data["login"],
                    data["password"],
                )

            self.refresh_employees_list()
            QMessageBox.information(self, "Успех", "Сотрудник добавлен!")

        modal = AddEmployeeModal(self, on_submit)
        modal.exec()

    def delete_employee(self):
        """Удаляет выбранного сотрудника."""
        selected_row = self.employees_table.currentRow()
        if selected_row == -1:
            QMessageBox.critical(self, "Ошибка", "Выберите сотрудника для удаления!")
            return

        employee_id = int(self.employees_table.item(selected_row, 0).text())

        with self.session_factory() as session:
            employee_service = EmployeeService(session)
            employee_service.delete_employee(employee_id)

        self.refresh_employees_list()
        QMessageBox.information(self, "Успех", "Сотрудник удален!")
