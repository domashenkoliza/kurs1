from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow
from services.auth_service import AuthService
from database.setup import SessionLocal


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 400, 200)

        # Подключение к базе данных
        self.session = SessionLocal()
        self.auth_service = AuthService(self.session)

        # Создание компоновки и виджетов
        self.layout = QVBoxLayout()

        self.login_label = QLabel("Логин")
        self.layout.addWidget(self.login_label)

        self.login_input = QLineEdit()
        self.layout.addWidget(self.login_input)

        self.password_label = QLabel("Пароль")
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Использование Enum
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Установка центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def login(self):
        """Проверка данных для входа."""
        login = self.login_input.text()
        password = self.password_input.text()

        if not (login and password):
            QMessageBox.critical(self, "Ошибка", "Заполните все поля")
            return

        user = self.auth_service.authenticate(login, password)
        if user:
            self.session.close()
            self.open_main_window()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")

    def open_main_window(self):
        """Открытие главного окна приложения."""
        self.close()  # Закрываем окно авторизации
        self.main_window = MainWindow()
        self.main_window.show()
