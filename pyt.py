from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, 
    QFormLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDateEdit, QDialog, QDialogButtonBox, QCheckBox, QAbstractItemView, QFileDialog
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
import sys

class ItemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Item')
        
        # Create widgets for Item Entry
        self.item_name_label = QLabel('Name:')
        self.item_name_input = QLineEdit()
        
        self.item_description_label = QLabel('Description:')
        self.item_description_input = QLineEdit()
        
        self.item_hsn_label = QLabel('HSN Code:')
        self.item_hsn_input = QLineEdit()
        
        self.item_quantity_label = QLabel('Quantity:')
        self.item_quantity_input = QLineEdit()
        
        self.item_unit_price_label = QLabel('Unit Price:')
        self.item_unit_price_input = QLineEdit()
        
        self.item_sgst_label = QLabel('SGST (%):')
        self.item_sgst_input = QLineEdit()
        
        self.item_cgst_label = QLabel('CGST (%):')
        self.item_cgst_input = QLineEdit()
        
        self.item_total_label = QLabel('Total:')
        self.item_total_input = QLineEdit()
        
        # Create buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        
        # Create layout for Item Entry
        item_form = QFormLayout()
        item_form.addRow(self.item_name_label, self.item_name_input)
        item_form.addRow(self.item_description_label, self.item_description_input)
        item_form.addRow(self.item_hsn_label, self.item_hsn_input)
        item_form.addRow(self.item_quantity_label, self.item_quantity_input)
        item_form.addRow(self.item_unit_price_label, self.item_unit_price_input)
        item_form.addRow(self.item_sgst_label, self.item_sgst_input)
        item_form.addRow(self.item_cgst_label, self.item_cgst_input)
        item_form.addRow(self.item_total_label, self.item_total_input)
        item_form.addWidget(self.button_box)
        
        self.setLayout(item_form)
        
        # Connect signals
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
    def get_item_data(self):
        return {
            'name': self.item_name_input.text(),
            'description': self.item_description_input.text(),
            'hsn_code': self.item_hsn_input.text(),
            'quantity': self.item_quantity_input.text(),
            'unit_price': self.item_unit_price_input.text(),
            'sgst': self.item_sgst_input.text(),
            'cgst': self.item_cgst_input.text(),
            'total': self.item_total_input.text()
        }

class InvoicePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize UI components
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Invoice Details')
        
        # Create headings
        self.billed_by_heading = QLabel('<b>Billed By</b>')
        self.billed_to_heading = QLabel('<b>Billed To</b>')
        self.invoice_details_heading = QLabel('<b>Invoice Details</b>')
        self.items_heading = QLabel('<b>Item Details</b>')
        
        # Create widgets for Billed By section
        self.billed_by_gst_label = QLabel('GST Number:')
        self.billed_by_gst_input = QLineEdit()
        self.billed_by_address_label = QLabel('Address:')
        self.billed_by_address_input = QLineEdit()
        self.billed_by_phone_label = QLabel('Phone Number:')
        self.billed_by_phone_input = QLineEdit()
        
        # Create widgets for Billed To section
        self.billed_to_gst_label = QLabel('GST Number:')
        self.billed_to_gst_input = QLineEdit()
        self.billed_to_address_label = QLabel('Address:')
        self.billed_to_address_input = QLineEdit()
        self.billed_to_phone_label = QLabel('Phone Number:')
        self.billed_to_phone_input = QLineEdit()
        
        # Create widgets for Invoice Details
        self.invoice_number_label = QLabel('Invoice Number:')
        self.invoice_number_input = QLineEdit()
        
        self.invoice_date_label = QLabel('Invoice Date:')
        self.invoice_date_input = QDateEdit()
        self.invoice_date_input.setDate(QDate.currentDate())  # Set default date to current date
        
        self.due_date_label = QLabel('Due Date:')
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate())  # Set default date to current date
        
        # Create widgets for Item Details Table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(9)  # Updated column count to include checkbox
        self.items_table.setHorizontalHeaderLabels([
            'Select All', 'Name', 'Description', 'HSN Code', 'Quantity', 
            'Unit Price', 'SGST (%)', 'CGST (%)', 'Total'
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Create header checkbox for bulk selection
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.setToolTip('Select/Deselect All')
        self.items_table.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.setCellWidget(0, 0, self.select_all_checkbox)
        self.select_all_checkbox.stateChanged.connect(self.select_all_items)
        
        self.items_table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        
        # Create Add Item button
        self.add_item_button = QPushButton('Add Item')
        
        # Create Delete Item button
        self.delete_item_button = QPushButton('Delete Selected Items')
        
        # Create Submit button
        self.submit_button = QPushButton('Submit')
        
        # Create Print button
        self.print_button = QPushButton('Print')
        
        # Create Export PDF button
        self.export_pdf_button = QPushButton('Export to PDF')
        
        # Create layouts for sections
        billed_by_form = QFormLayout()
        billed_by_form.addRow(self.billed_by_gst_label, self.billed_by_gst_input)
        billed_by_form.addRow(self.billed_by_address_label, self.billed_by_address_input)
        billed_by_form.addRow(self.billed_by_phone_label, self.billed_by_phone_input)
        
        billed_to_form = QFormLayout()
        billed_to_form.addRow(self.billed_to_gst_label, self.billed_to_gst_input)
        billed_to_form.addRow(self.billed_to_address_label, self.billed_to_address_input)
        billed_to_form.addRow(self.billed_to_phone_label, self.billed_to_phone_input)
        
        invoice_form = QFormLayout()
        invoice_form.addRow(self.invoice_number_label, self.invoice_number_input)
        invoice_form.addRow(self.invoice_date_label, self.invoice_date_input)
        invoice_form.addRow(self.due_date_label, self.due_date_input)
        
        # Create group boxes for sections
        billed_by_group = QGroupBox()
        billed_by_group.setTitle('Billed By')
        billed_by_group.setLayout(billed_by_form)
        
        billed_to_group = QGroupBox()
        billed_to_group.setTitle('Billed To')
        billed_to_group.setLayout(billed_to_form)
        
        invoice_group = QGroupBox()
        invoice_group.setTitle('Invoice Details')
        invoice_group.setLayout(invoice_form)
        
        # Horizontal layout to position sections side-by-side
        top_layout = QHBoxLayout()
        top_layout.addWidget(billed_by_group)
        top_layout.addWidget(billed_to_group)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(invoice_group)
        main_layout.addWidget(self.items_heading)
        main_layout.addWidget(self.items_table)
        main_layout.addWidget(self.add_item_button)  # Add button below items table
        main_layout.addWidget(self.delete_item_button)  # Delete button below add item button
        main_layout.addWidget(self.submit_button)  # Submit button
        main_layout.addWidget(self.print_button)  # Print button
        main_layout.addWidget(self.export_pdf_button)  # Export PDF button
        
        # Set main layout
        self.setLayout(main_layout)
        
        # Apply Meta-like color scheme
        style_sheet = """QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #2c3e50; /* Darker text color for better readability */
    background-color: #f4f6f9; /* Light background color for the entire window */
}

QLabel {
    color: #34495e; /* Slightly darker shade for labels */
    font-weight: bold; /* Bold text for labels to make them stand out */
    padding-bottom: 5px; /* Add padding below labels for better spacing */
}

QLineEdit, QDateEdit {
    border: 1px solid #bdc3c7; /* Light gray border */
    border-radius: 5px;
    padding: 8px;
    background-color: #ffffff; /* White background for input fields */
    color: #2c3e50; /* Darker text color for input fields */
}

QPushButton {
    background-color: #3498db; /* Soft blue button color */
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9; /* Darker blue on hover */
}

QTableWidget {
    border: 1px solid #bdc3c7;
    background-color: #ffffff;
    gridline-color: #e0e0e0; /* Light gray gridlines for better separation */
}

QTableWidget QHeaderView::section {
    background-color: #3498db; /* Soft blue header color */
    color: white;
    font-weight: bold; /* Bold text for headers */
    padding: 10px; /* Add padding for better spacing */
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #bdc3c7;
    border-radius: 5px;
    margin-bottom: 20px; /* Increased margin for better separation */
    padding: 10px; /* Added padding inside group boxes */
    background-color: #ffffff; /* White background for group boxes */
}

QGroupBox:title {
    subcontrol-position: top center;
    padding: 0px; /* Increased padding for better visibility */
    background-color: #ecf0f1; /* Light gray background for the title area */
    color: #3498db; /* Soft blue for the title text */
    font-size: 16px; /* Increased font size for better readability */
}

QCheckBox {
    padding: 5px;
}

QDialogButtonBox {
    button-layout: QDialogButtonBox::ActionRole;
}
        """


        self.setStyleSheet(style_sheet)
        
        # Connect button signals
        self.add_item_button.clicked.connect(self.open_add_item_dialog)
        self.delete_item_button.clicked.connect(self.delete_selected_items)
        self.submit_button.clicked.connect(self.submit_invoice)
        self.print_button.clicked.connect(self.print_invoice)
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        
    def select_all_items(self, state):
        """Select or deselect all items in the table."""
        for row in range(self.items_table.rowCount()):
            checkbox = self.items_table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(state == Qt.CheckState.Checked)
    
    def open_add_item_dialog(self):
        dialog = ItemDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item_data = dialog.get_item_data()
            self.add_item_to_table(item_data)
            
    def add_item_to_table(self, item_data):
        row_position = self.items_table.rowCount()
        self.items_table.insertRow(row_position)
        
        # Add checkbox to the first column
        checkbox = QCheckBox()
        self.items_table.setCellWidget(row_position, 0, checkbox)
        
        self.items_table.setItem(row_position, 1, QTableWidgetItem(item_data['name']))
        self.items_table.setItem(row_position, 2, QTableWidgetItem(item_data['description']))
        self.items_table.setItem(row_position, 3, QTableWidgetItem(item_data['hsn_code']))
        self.items_table.setItem(row_position, 4, QTableWidgetItem(item_data['quantity']))
        self.items_table.setItem(row_position, 5, QTableWidgetItem(item_data['unit_price']))
        self.items_table.setItem(row_position, 6, QTableWidgetItem(item_data['sgst']))
        self.items_table.setItem(row_position, 7, QTableWidgetItem(item_data['cgst']))
        self.items_table.setItem(row_position, 8, QTableWidgetItem(item_data['total']))
        
    def delete_selected_items(self):
        selected_rows = []
        for row in range(self.items_table.rowCount()):
            checkbox = self.items_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
                
        for row in reversed(selected_rows):  # Delete rows in reverse to avoid index issues
            self.items_table.removeRow(row)
    
    def submit_invoice(self):
        QMessageBox.information(self, "Submit", "Invoice submitted successfully!")
    
    def print_invoice(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.render_invoice(printer)
    
    def render_invoice(self, printer):
        painter = QPainter(printer)
        screen = self.grab()
        painter.drawPixmap(10, 10, screen)
        painter.end()
    
    def export_to_pdf(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("PDF files (*.pdf)")
        file_dialog.setDefaultSuffix("pdf")
        
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_name = file_dialog.selectedFiles()[0]
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_name)
            self.render_invoice(printer)

def main():
    app = QApplication(sys.argv)
    window = InvoicePage()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
