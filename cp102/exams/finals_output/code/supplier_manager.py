import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
    QLabel, QMessageBox, QAction, QMenuBar
)
import theme
from inventory import InventoryDB, DB_CONFIG

class SupplierManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Supplier Manager")
        self.resize(920, 680)

        # Theme toggle in menu
        mb = QMenuBar(self)
        self.setMenuBar(mb)
        view = mb.addMenu("View")
        t = QAction("Toggle Theme", self)
        t.triggered.connect(lambda: theme.toggle(QApplication.instance()))
        view.addAction(t)

        # Central layout
        cw = QWidget()
        self.setCentralWidget(cw)
        v = QVBoxLayout(cw)

        # Table
        self.tableSuppliers = QTableWidget(0, 3)
        self.tableSuppliers.setHorizontalHeaderLabels(["ID", "Name", "Contact"])
        v.addWidget(self.tableSuppliers)

        # Form inputs
        form = QHBoxLayout()
        form.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        form.addWidget(self.name_input)
        form.addWidget(QLabel("Contact:"))
        self.contact_input = QLineEdit()
        form.addWidget(self.contact_input)
        v.addLayout(form)

        # Buttons
        btns = QHBoxLayout()
        self.btnAdd = QPushButton("Add")
        self.btnUpdate = QPushButton("Update")
        self.btnDelete = QPushButton("Delete")
        self.btnRefresh = QPushButton("Refresh")
        for btn in (self.btnAdd, self.btnUpdate, self.btnDelete, self.btnRefresh):
            btns.addWidget(btn)
        v.addLayout(btns)

        # Use the same DB class and configuration as inventory.py
        self.db = InventoryDB(**DB_CONFIG)

        # Wire up signals
        self.btnAdd.clicked.connect(self.add_supplier)
        self.btnUpdate.clicked.connect(self.update_supplier)
        self.btnDelete.clicked.connect(self.delete_supplier)
        self.btnRefresh.clicked.connect(self.load_suppliers)
        self.tableSuppliers.currentCellChanged.connect(self.on_select)

        # Initial load
        self.load_suppliers()

    def add_supplier(self):
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        if not name:
            return QMessageBox.warning(self, "Input Error", "Name required.")
        sid = self.db.create_supplier(name, contact)
        QMessageBox.information(self, "Added", f"Supplier ID {sid}")
        self.load_suppliers()

    def update_supplier(self):
        row = self.tableSuppliers.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Select", "Select a supplier first.")
        sid = int(self.tableSuppliers.item(row, 0).text())
        name = self.name_input.text().strip()
        contact = self.contact_input.text().strip()
        self.db.update_supplier(sid, name=name, contact=contact)
        QMessageBox.information(self, "Updated", "Supplier updated.")
        self.load_suppliers()

    def delete_supplier(self):
        row = self.tableSuppliers.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Select", "Select a supplier first.")
        sid = int(self.tableSuppliers.item(row, 0).text())
        self.db.delete_supplier(sid)
        QMessageBox.information(self, "Deleted", "Supplier deleted.")
        self.load_suppliers()

    def load_suppliers(self):
        recs = self.db.read_suppliers()
        self.tableSuppliers.setRowCount(0)
        for sid, name, contact in recs:
            r = self.tableSuppliers.rowCount()
            self.tableSuppliers.insertRow(r)
            self.tableSuppliers.setItem(r, 0, QTableWidgetItem(str(sid)))
            self.tableSuppliers.setItem(r, 1, QTableWidgetItem(name))
            self.tableSuppliers.setItem(r, 2, QTableWidgetItem(contact))
        self.tableSuppliers.resizeColumnsToContents()
        self.tableSuppliers.resizeRowsToContents()

    def on_select(self, row, col):
        if row < 0:
            return
        self.name_input.setText(self.tableSuppliers.item(row, 1).text())
        self.contact_input.setText(self.tableSuppliers.item(row, 2).text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    theme.setup(app)
    w = SupplierManagerWindow()
    w.show()
    sys.exit(app.exec_())
