import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QAction, QMenuBar
)
import theme
from inventory import InventoryWindow
from supplier_manager import SupplierManagerWindow

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        # Make it big and docked top-left
        self.setGeometry(500, 300, 720, 440)

        # Central widget + layout
        cw = QWidget()
        self.setCentralWidget(cw)
        layout = QVBoxLayout(cw)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Buttons
        self.btnInventory = QPushButton("Manage Inventory")
        self.btnSuppliers = QPushButton("Manage Suppliers")
        self.btnExit      = QPushButton("Exit")

        for btn in (self.btnInventory, self.btnSuppliers, self.btnExit):
            btn.setMinimumHeight(60)
            layout.addWidget(btn)

        # Button signals
        self.btnInventory.clicked.connect(self.open_inventory)
        self.btnSuppliers.clicked.connect(self.open_suppliers)
        self.btnExit.clicked.connect(self.close)

        # Menu bar with Theme toggle and Exit
        mb = QMenuBar(self)
        self.setMenuBar(mb)
        file_menu = mb.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view = mb.addMenu("View")
        toggle = QAction("Toggle Theme", self)
        toggle.triggered.connect(lambda: theme.toggle(QApplication.instance()))
        view.addAction(toggle)

    def open_inventory(self):
        self.inv_win = InventoryWindow()
        self.inv_win.show()

    def open_suppliers(self):
        self.sup_win = SupplierManagerWindow()
        self.sup_win.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    theme.setup(app)
    w = MainMenu()
    w.show()
    sys.exit(app.exec_())
