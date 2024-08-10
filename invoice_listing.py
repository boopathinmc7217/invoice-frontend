from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class InvoiceListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Invoice List')
        self.setGeometry(100, 100, 600, 400)
        
        # Create table widget to display invoices
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Invoice Number', 'Date', 'Total Amount', 'Status'])
        
        # Create search fields
        self.invoice_number_input = QLineEdit()
        self.invoice_number_input.setPlaceholderText('Invoice Number')
        
        self.billed_to_input = QLineEdit()
        self.billed_to_input.setPlaceholderText('Billed To')
        
        # Create Search button
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_invoices)
        
        # Create layout and add widgets
        layout = QVBoxLayout()
        
        # Add search fields and button to layout
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.invoice_number_input)
        search_layout.addWidget(self.billed_to_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        
        # Add table to layout
        layout.addWidget(self.table)
        
        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # Maximize button
        self.maximize_button = QPushButton('Maximize')
        self.maximize_button.clicked.connect(self.toggle_maximize)
        button_layout.addWidget(self.maximize_button)
        
        # Close button
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Load initial data
        self.all_invoices = self.load_data()
        self.update_table(self.all_invoices)

    def load_data(self):
        # Dummy data; replace with actual data retrieval logic
        invoices = [
            {"number": "INV001", "date": "2024-08-01", "total": "500.00", "status": "Paid", "billed_to": "Customer A"},
            {"number": "INV002", "date": "2024-08-05", "total": "300.00", "status": "Unpaid", "billed_to": "Customer B"},
            # Add more dummy data as needed
        ]
        return invoices

    def search_invoices(self):
        invoice_number = self.invoice_number_input.text().strip()
        billed_to = self.billed_to_input.text().strip()
        
        filtered_invoices = [inv for inv in self.all_invoices
                             if (invoice_number in inv["number"] or not invoice_number) and
                                (billed_to in inv["billed_to"] or not billed_to)]
        
        self.update_table(filtered_invoices)

    def update_table(self, invoices):
        self.table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(invoice["number"]))
            self.table.setItem(row, 1, QTableWidgetItem(invoice["date"]))
            self.table.setItem(row, 2, QTableWidgetItem(invoice["total"]))
            self.table.setItem(row, 3, QTableWidgetItem(invoice["status"]))

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText('Maximize')
        else:
            self.showMaximized()
            self.maximize_button.setText('Restore')
