import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from gui.login_window import LoginWindow
from database.setup import init_db


def handle_exception(exc_type, exc_value, exc_traceback):
    """Обработчик необработанных исключений."""
    # Log the exception in the console for debugging
    print(f"Error: {exc_value}", file=sys.stderr)
    error_message = f"Произошла ошибка:\n{exc_value}"
    
    # Ensure QApplication is running before showing the dialog
    if QApplication.instance():
        error_dialog = QMessageBox()
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(error_message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.exec()
    else:
        # If QApplication is not active, print to console
        print("Critical Error:", error_message, file=sys.stderr)


def load_styles(app):
    """Загрузка стилей приложения."""
    try:
        with open("./src/gui/styles.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("Файл стилей не найден. Приложение будет работать без стилей.")


def main():
    # Initialize database
    init_db()

    # Set the exception hook to handle uncaught exceptions
    sys.excepthook = handle_exception

    # Create the application
    app = QApplication(sys.argv)

    # Load styles
    load_styles(app)

    # Create and show the login window
    login_window = LoginWindow()
    login_window.show()

    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
