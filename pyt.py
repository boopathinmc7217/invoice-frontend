from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, 
    QFormLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDateEdit, QDialog,QCheckBox, QAbstractItemView, QFileDialog, QMenuBar, QMenu
)
from PyQt6.QtCore import QDate, Qt


from PyQt6.QtGui import QPainter,QAction
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
import sys

from invoice_listing import InvoiceListDialog
from item_dialog_box import ItemDialog
from login import LoginPage
from stylesheet import STYLESHEET
class InvoicePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize UI components
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Invoice Details')
        menu_bar = QMenuBar(self)
        actions_menu = QMenu('Actions', self)
        view_menu = QMenu('View', self)
        menu_bar.addMenu(view_menu)
        
        # Add Invoice List action to View menu
        self.invoice_list_action = QAction('Invoice List', self)
        self.invoice_list_action.triggered.connect(self.show_invoice_list_dialog)
        view_menu.addAction(self.invoice_list_action)
        menu_bar.addMenu(actions_menu)
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
        self.items_table.setColumnCount(10)  # Updated column count to include checkbox
        self.items_table.setHorizontalHeaderLabels([
           "",'Name', 'Description', 'HSN Code', 'Quantity', 
            'Unit Price', 'GST(%)','SGST (%)', 'CGST (%)', 'Total'
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

        self.delete_action = QAction('Delete Selected Items', self)
        self.delete_action.triggered.connect(self.delete_selected_items)
        actions_menu.addAction(self.delete_action)
        
        self.submit_action = QAction('Submit', self)
        self.submit_action.triggered.connect(self.submit_invoice)
        actions_menu.addAction(self.submit_action)
        
        self.print_action = QAction('Print', self)
        self.print_action.triggered.connect(self.print_invoice)
        actions_menu.addAction(self.print_action)
        
        self.export_pdf_action = QAction('Export to PDF', self)
        self.export_pdf_action.triggered.connect(self.export_to_pdf)
        actions_menu.addAction(self.export_pdf_action)

        # List dialog box
        # self.invoice_list_action = QAction('Invoice List', self)
        # self.invoice_list_action.triggered.connect(self.show_invoice_list_dialog)
        # actions_menu.addAction(self.invoice_list_action)

        # Set main layout
        self.setLayout(main_layout)
        
        # Apply Meta-like color scheme
        self.setStyleSheet(STYLESHEET)
        
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
        self.items_table.setItem(row_position, 6, QTableWidgetItem(item_data['gst']))
        self.items_table.setItem(row_position, 7, QTableWidgetItem(item_data['sgst']))
        self.items_table.setItem(row_position, 8, QTableWidgetItem(item_data['cgst']))
        self.items_table.setItem(row_position, 9, QTableWidgetItem(item_data['total']))
        
    def delete_selected_items(self):
        selected_rows = []
        for row in range(self.items_table.rowCount()):
            checkbox = self.items_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)
                
        for row in reversed(selected_rows):  # Delete rows in reverse to avoid index issues
            self.items_table.removeRow(row)

    def show_invoice_list_dialog(self):
        dialog = InvoiceListDialog(self)
        dialog.exec()

    
    def submit_invoice(self):
        invoice_holder = {}
        invoice_holder["billed_by_gst"] = self.billed_by_gst_input.text()
        invoice_holder["billed_by_address"] = self.billed_by_address_input.text()
        invoice_holder["billed_by_phone"] = self.billed_by_phone_input.text()
        invoice_holder["billed_to_gst"] = self.billed_to_gst_input.text()
        invoice_holder["billed_to_address"] = self.billed_to_address_input.text()
        invoice_holder["billed_to_phone"] = self.billed_to_phone_input.text()
        invoice_holder["invoice_number"] = self.invoice_number_input.text()
        invoice_holder["invoice_date"] = self.invoice_date_input.date().toString("yyyy-MM-dd")
        invoice_holder["due_date"] = self.due_date_input.date().toString("yyyy-MM-dd")
        invoice_holder["items"] = []
        for row in range(self.items_table.rowCount()):
            items_holder = {}
            items_holder["name"] = self.items_table.item(row, 1).text()
            items_holder["description"] = self.items_table.item(row, 2).text()
            items_holder["hsn_code"] = self.items_table.item(row, 3).text()
            items_holder["quantity"] = self.items_table.item(row, 4).text()
            items_holder["unit_price"] = self.items_table.item(row, 5).text()
            items_holder["gst"] = self.items_table.item(row, 6).text()
            items_holder["sgst"] = self.items_table.item(row, 7).text()
            items_holder["cgst"] = self.items_table.item(row, 8).text()
            items_holder["total"] = self.items_table.item(row, 9).text()
            invoice_holder["items"].append(items_holder)
        print(invoice_holder)
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

    login_window = LoginPage()
    if login_window.exec()==QDialog.DialogCode.Accepted:
        main_window = InvoicePage()
        main_window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    main()