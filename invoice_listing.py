import json
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QHeaderView


from config import AppConfig
from preview import InvoicePreviewDialog
from request_manager import RequestManager
from save_files_local import SaveInvoiceLocally  # Assuming you have a class for managing API requests

class InvoiceListDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Invoice List')
        self.setGeometry(100, 100, 600, 400)
        self.monitoring_scroll_position = True
        # Create table widget to display invoices
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Invoice Number', 'Issued Date', "Billed To", 'Due Date', 'Total Amount'])
        
        # Make all columns equal in width
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
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

        # Connect only once to avoid multiple signal connections
        self.table.doubleClicked.connect(self.on_item_double_clicked)

        # Monitor scrolling to trigger API call
        if self.monitoring_scroll_position:
            self.table.verticalScrollBar().valueChanged.connect(self.check_scroll_position)
        
    def load_data(self):
        invoice_path = AppConfig().get_invoice_path()
        invoices = []
        with open(invoice_path, 'r') as file:
            for line in file: 
                invoice_dict = SaveInvoiceLocally().decrypt_data(line.strip())
                invoice_dict = json.loads(invoice_dict)
                invoice = {
                    "Invoice Number": invoice_dict["invoice_number"],
                    "Issued Date": invoice_dict["invoice_date"],
                    "Total Amount": invoice_dict["Total bill"],
                    "Billed To": invoice_dict["billed_to_gst"],
                    "Due Date": invoice_dict["due_date"]
                }
                invoices.append(invoice)
        return invoices

    def search_invoices(self):
        invoice_number = self.invoice_number_input.text().strip()
        billed_to = self.billed_to_input.text().strip()
        
        filtered_invoices = [inv for inv in self.all_invoices
                             if (invoice_number in inv["Invoice Number"] or not invoice_number) and
                                (billed_to in inv["Billed To"] or not billed_to)]
        
        self.update_table(filtered_invoices)

    def update_table(self, invoices):
        self.table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            self.table.setItem(row, 0, QTableWidgetItem(invoice["Invoice Number"]))
            self.table.setItem(row, 1, QTableWidgetItem(invoice["Issued Date"]))
            self.table.setItem(row, 2, QTableWidgetItem(invoice["Billed To"]))
            self.table.setItem(row, 3, QTableWidgetItem(invoice["Due Date"]))
            self.table.setItem(row, 4, QTableWidgetItem(invoice["Total Amount"]))


    def on_item_double_clicked(self, index):
        row = index.row()
        invoice_number = self.table.item(row, 0).text()
        
        # Find the invoice data for the selected row
        invoice_data = next((inv for inv in self.all_invoices if inv["Invoice Number"] == invoice_number), None)
        if invoice_data:
            # Create and show the preview dialog
            preview_dialog = InvoicePreviewDialog(invoice_data, self)
            preview_dialog.exec()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText('Maximize')
        else:
            self.showMaximized()
            self.maximize_button.setText('Restore')
    
    def check_scroll_position(self):
        if self.table.rowCount() > 6 and self.table.verticalScrollBar().value() > self.table.verticalScrollBar().maximum() - 50 and self.monitoring_scroll_position:
            self.load_more_invoices()
            self.monitoring_scroll_position = False
    def load_more_invoices(self):
        # This is where you'd call your API to get more invoices
        request_manager = RequestManager()
        additional_invoices = request_manager.get(endpoint=f"insert-invoices/?start=f'{len(self.all_invoices)}'")
        if additional_invoices:
            self.all_invoices.extend(additional_invoices)
            self.update_table(self.all_invoices)
