from PyQt6.QtWidgets import QMainWindow, QTabWidget
from gui.tabs.clients_tab import ClientsTab
from gui.tabs.employees_tab import EmployeesTab
from gui.tabs.orders_tab import OrdersTab
from gui.tabs.repairs_tab import RepairsTab
from gui.tabs.shoes_tab import ShoesTab
from gui.tabs.service_journal_tab import ServiceJournalTab
from database.setup import SessionLocal


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ремонтная мастерская")
        self.setGeometry(200, 200, 1024, 768)

        self.session_factory = SessionLocal

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Вкладки
        self.clients_tab = ClientsTab(self.session_factory)
        self.tab_widget.addTab(self.clients_tab, "Клиенты")

        self.employees_tab = EmployeesTab(self.session_factory)
        self.tab_widget.addTab(self.employees_tab, "Сотрудники")

        self.orders_tab = OrdersTab(self.session_factory)
        self.tab_widget.addTab(self.orders_tab, "Заказы")

        self.repairs_tab = RepairsTab(self.session_factory)
        self.tab_widget.addTab(self.repairs_tab, "Ремонты")

        self.shoes_tab = ShoesTab(self.session_factory)
        self.tab_widget.addTab(self.shoes_tab, "Обувь")

        self.services_journal_tab = ServiceJournalTab(self.session_factory)
        self.tab_widget.addTab(self.services_journal_tab, "Услуги")

        # Connect the signal to the refresh method
        self.tab_widget.currentChanged.connect(self.refresh_active_tab)

    def refresh_active_tab(self, index):
        """Refresh the active tab when the user switches tabs."""
        current_widget = self.tab_widget.widget(index)

        # Call a `refresh` method for the current tab if it exists
        if hasattr(current_widget, "refresh"):
            current_widget.refresh()
