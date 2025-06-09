import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QAction, QMenuBar
from PyQt5.QtCore import Qt, QEvent
import pymysql
import theme

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Password123456',
    'database': 'inventory_db'
}

class InventoryDB:

    def __init__(self, host, user, password, database):
        self.conn = pymysql.connect(
            host=host, user=user, password=password,
            database=database, cursorclass=pymysql.cursors.Cursor
        )

    def close(self):
        self.conn.close()

    def create_supplier(self, name, contact):

        with self.conn.cursor() as cur:

            cur.execute("""
                SELECT supplier_id FROM suppliers
                WHERE supplier_name = %s AND contact = %s
            """, (name, contact))
            row = cur.fetchone()

            if row:

                return row[0]  # Already exists

            cur.execute("""
                INSERT INTO suppliers (supplier_name, contact)
                VALUES (%s, %s)
            """, (name, contact))

        self.conn.commit()
        return cur.lastrowid
    
    def read_suppliers(self):
        
        with self.conn.cursor() as cur:
            cur.execute("SELECT supplier_id, supplier_name, contact FROM suppliers")
        
            return cur.fetchall()
    
    def read_active_suppliers(self):
        """Return suppliers that still have at least one item."""
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT s.supplier_id, s.supplier_name, s.contact
                FROM suppliers s
                JOIN items i ON s.supplier_id = i.supplier_id
            """)
        
            return cur.fetchall()

    def update_supplier(self, supplier_id, name=None, contact=None):
        fields = {}
        
        if name is not None:
            fields['supplier_name'] = name
       
        if contact is not None:
            fields['contact'] = contact
        
        if not fields:
            return
        
        cols = ", ".join(f"{k}=%s" for k in fields)
        vals = list(fields.values()) + [supplier_id]
        
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE suppliers SET {cols} WHERE supplier_id=%s", vals)
        
        self.conn.commit()

    def delete_supplier(self, supplier_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
        self.conn.commit()

    def create_item(self, barcode, name, qty, price, brand, sup_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT barcode FROM items WHERE barcode=%s", (barcode,))
            if cur.fetchone():
                return False
            cur.execute(
                "INSERT INTO items (barcode,name,quantity,price,brand,supplier_id) "
                "VALUES (%s,%s,%s,%s,%s,%s)",
                (barcode, name, qty, price, brand, sup_id)
            )
        self.conn.commit()
        return True

    def read_items(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT i.barcode, i.name, i.quantity, i.price, i.brand, "
                "s.supplier_name FROM items i "
                "LEFT JOIN suppliers s ON i.supplier_id=s.supplier_id"
            )
            return cur.fetchall()

    def update_item(self, barcode, **fields):
        if not fields:
            return
        cols = ", ".join(f"{k}=%s" for k in fields)
        vals = list(fields.values()) + [barcode]
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE items SET {cols} WHERE barcode=%s", vals)
        self.conn.commit()

    def delete_item(self, barcode):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM items WHERE barcode=%s", (barcode,))
        self.conn.commit()

# — GUI layer —————————————————

class InventoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'invGUI.ui'), self)

        # Theme toggle
        mb = QMenuBar(self)
        self.setMenuBar(mb)
        view = mb.addMenu("View")
        toggle = QAction("Toggle Theme", self)
        toggle.triggered.connect(lambda: theme.toggle(QApplication.instance()))
        view.addAction(toggle)

        # Spinbox range
        if hasattr(self,'quantity_filter_input'):
            self.quantity_filter_input.setMaximum(1_000_000)

        # DB
        self.db = InventoryDB(**DB_CONFIG)
        self.current_row = 0

        # Field navigation
        self.barcode_input.returnPressed.connect(self.name_input.setFocus)
        self.name_input.returnPressed.connect(self.quantity_input.setFocus)
        self.quantity_input.returnPressed.connect(self.price_input.setFocus)
        self.price_input.returnPressed.connect(self.brand_input.setFocus)
        self.brand_input.returnPressed.connect(self.supplier_name_input.setFocus)
        self.supplier_name_input.returnPressed.connect(self.supplier_contact_input.setFocus)
        self.supplier_contact_input.returnPressed.connect(self.create_item)

        # Buttons
        self.add_or_create_button.clicked.connect(self.create_item)
        self.update_button.clicked.connect(self.update_item)
        self.delete_button.clicked.connect(self.delete_item)
        self.refresh_button.clicked.connect(lambda: self.load_items(None))
        self.previous_button.clicked.connect(self.on_previous)
        self.next_button.clicked.connect(self.on_next)
        self.first_button.clicked.connect(self.on_first)
        self.last_button.clicked.connect(self.on_last)

        # Table
        self.table.currentCellChanged.connect(self.on_item_select)
        self.table.installEventFilter(self)
        if hasattr(self,'quantity_filter_input'):
            self.quantity_filter_input.editingFinished.connect(self.apply_filter)

        # Initialize
        self.load_items(None)
        self.load_suppliers()
        self.table.setFocus()
        if self.table.rowCount(): self.table.selectRow(0)

    def create_item(self):
        
        if not (b:=self.barcode_input.text().strip()) or not (n:=self.name_input.text().strip()) or not (qt:=self.quantity_input.text().strip()):
            return QMessageBox.warning(self,"Input Error","Barcode, Name & Quantity required.")
        
        try:
            q=int(qt); p=float(self.price_input.text() or 0.0)
            br=self.brand_input.text().strip()
            sup=self.supplier_name_input.text().strip()
            c=self.supplier_contact_input.text().strip()
        
        except Exception as e:
            return QMessageBox.warning(self,"Input Error",str(e))

        sid=self.db.create_supplier(sup,c)
        
        if not self.db.create_item(b,n,q,p,br,sid):
            return QMessageBox.warning(self,"Duplicate","Barcode exists.")
        QMessageBox.information(self,"Success","Item added.")
        self._clear_inputs()
        self.load_items(None); self.load_suppliers()
        last=self.table.rowCount()-1
        
        if last>=0: self.table.setCurrentCell(last,0)
        self.table.setFocus()

    def apply_filter(self):
        self.load_items(self.quantity_filter_input.value())

    def load_items(self, max_q):
        self.table.setRowCount(0)
        for rec in self.db.read_items():
            if max_q is None or rec[2]<=max_q:
                r=self.table.rowCount(); self.table.insertRow(r)
                for c,v in enumerate(rec):
                    self.table.setItem(r,c,QTableWidgetItem(str(v)))
        row=min(self.current_row,self.table.rowCount()-1)
        if row>=0:
            self.table.setCurrentCell(row,0)
            self.table.scrollToItem(self.table.item(row,0))

    def load_suppliers(self):
        self.tableWidget.setRowCount(0)
        for rec in self.db.read_active_suppliers():
            r=self.tableWidget.rowCount(); self.tableWidget.insertRow(r)
            for c,v in enumerate(rec):
                self.tableWidget.setItem(r,c,QTableWidgetItem(str(v)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def on_item_select(self,row,col,*_):
        if row<0: return
        self.current_row=row
        self.barcode_input.setText(self.table.item(row,0).text())
        self.name_input.setText(self.table.item(row,1).text())
        self.quantity_input.setText(self.table.item(row,2).text())
        self.price_input.setText(self.table.item(row,3).text())
        self.brand_input.setText(self.table.item(row,4).text())
        self.supplier_name_input.setText(self.table.item(row,5).text())

    def on_first(self):
        if self.table.rowCount(): self.table.setCurrentCell(0,0)
    def on_last(self):
        last=self.table.rowCount()-1
        if last>=0: self.table.setCurrentCell(last,0)
    def on_next(self):
        r,c=self.table.currentRow(),self.table.currentColumn()
        self.table.setCurrentCell(min(r+1,self.table.rowCount()-1),c)
    def on_previous(self):
        r,c=self.table.currentRow(),self.table.currentColumn()
        self.table.setCurrentCell(max(r-1,0),c)

    def update_item(self):
        b=self.barcode_input.text().strip()
        fields={}
        if self.name_input.text(): fields['name']=self.name_input.text().strip()
        if self.quantity_input.text(): fields['quantity']=int(self.quantity_input.text())
        if self.price_input.text(): fields['price']=float(self.price_input.text())
        if self.brand_input.text(): fields['brand']=self.brand_input.text().strip()
        if self.supplier_name_input.text():
            sid=self.db.create_supplier(
                self.supplier_name_input.text().strip(),
                self.supplier_contact_input.text().strip()
            )
            fields['supplier_id']=sid
        if fields:
            self.db.update_item(b,**fields)
            QMessageBox.information(self,"Updated","Item updated.")
            self._clear_inputs(); self.load_items(None); self.load_suppliers()
            self.table.setFocus()
        else:
            QMessageBox.warning(self,"No Changes","Modify at least one field.")

    def delete_item(self):
        b=self.barcode_input.text().strip()
        self.db.delete_item(b)
        QMessageBox.information(self,"Deleted","Item deleted.")
        self._clear_inputs(); self.load_items(None); self.load_suppliers()
        self.table.setFocus()

    def _clear_inputs(self):
        for w in (self.barcode_input,self.name_input,self.quantity_input,
                  self.price_input,self.brand_input,
                  self.supplier_name_input,self.supplier_contact_input):
            w.clear()
            
    def update_supplier(self, supplier_id, name=None, contact=None):
        """Update name and/or contact of a supplier by ID."""
        fields = {}
        if name is not None:
            fields['supplier_name'] = name
        if contact is not None:
            fields['contact'] = contact
        if not fields:
            return
        cols = ", ".join(f"{k}=%s" for k in fields)
        vals = list(fields.values()) + [supplier_id]
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE suppliers SET {cols} WHERE supplier_id=%s", vals)
        self.conn.commit()

    def delete_supplier(self, supplier_id):
        """Delete a supplier by ID."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
        self.conn.commit()
        
    def eventFilter(self,src,event):
        if src is self.table and event.type()==QEvent.KeyPress:
            r,c=self.table.currentRow(),self.table.currentColumn()
            if event.key()==Qt.Key_Right:
                self.table.setCurrentCell(min(r+1,self.table.rowCount()-1),c);return True
            if event.key()==Qt.Key_Left:
                self.table.setCurrentCell(max(r-1,0),c);return True
        return super().eventFilter(src,event)

    def keyPressEvent(self,event):
        r,c=self.table.currentRow(),self.table.currentColumn()
        if event.key()==Qt.Key_Down:
            self.table.setCurrentCell(min(r+1,self.table.rowCount()-1),c)
        elif event.key()==Qt.Key_Up:
            self.table.setCurrentCell(max(r-1,0),c)
        else:
            super().keyPressEvent(event)

    def closeEvent(self,ev):
        self.db.close(); super().closeEvent(ev)
