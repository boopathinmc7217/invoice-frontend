from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QVBoxLayout,
    QFormLayout, QLabel, QHBoxLayout, QMessageBox, QGroupBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDateEdit, QDialog, QCheckBox, QAbstractItemView, QFileDialog, QMenuBar, QMenu,QComboBox
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPainter, QAction
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
import sys

from biller_info_dialog import BillerInfoDialog
from config import AppConfig
from customer_info_dialog import CustomerInfoDialog
from invoice_listing import InvoiceListDialog
from item_dialog_box import ItemDialog
from login import LoginPage
from request_manager import RequestManager
from save_files_local import SaveInvoiceLocally
from stylesheet import STYLESHEET


class InvoicePage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()
        self.file_ops = SaveInvoiceLocally()
        self.populate_dropdowns()



    def init_ui(self):
        self.biller_info =[]
        self.customer_info =[]
        self.setWindowTitle('Invoice Details')

        # Create menu bar and actions
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        actions_menu = QMenu('Actions', self)
        view_menu = QMenu('View', self)
        self.menu_bar.addMenu(view_menu)

        # Add Invoice List action to View menu
        self.invoice_list_action = QAction('Invoice List', self)
        self.invoice_list_action.triggered.connect(
            self.show_invoice_list_dialog)
        view_menu.addAction(self.invoice_list_action)
        self.menu_bar.addMenu(actions_menu)

        # Create headings
        self.billed_by_heading = QLabel('<b>Billed By</b>')
        self.billed_to_heading = QLabel('<b>Billed To</b>')
        self.invoice_details_heading = QLabel('<b>Invoice Details</b>')
        self.items_heading = QLabel('<b>Item Details</b>')

        # Create widgets for Billed By section
        self.billed_by_cname_label = QLabel('Company Name:')
        self.billed_by_cname_input = QLineEdit()
        self.billed_by_gst_label = QLabel('GST Number:')
        self.billed_by_gst_input = QLineEdit()
        self.billed_by_address_label = QLabel('Address:')
        self.billed_by_address_input = QLineEdit()
        self.billed_by_phone_label = QLabel('Phone Number:')
        self.billed_by_phone_input = QLineEdit()
        self.billed_by_pan_label = QLabel('PAN:')
        self.billed_by_pan_input = QLineEdit()
        self.billed_by_email_label = QLabel('Email:')
        self.billed_by_email_input = QLineEdit()

        self.total_amount_label = QLabel('<b>Total Amount:</b> $0.00')
        # Create widgets for Billed To section
        self.billed_to_cname_label = QLabel('Company Name:')
        self.billed_to_cname_input = QLineEdit()
        self.billed_to_gst_label = QLabel('GST Number:')
        self.billed_to_gst_input = QLineEdit()
        self.billed_to_address_label = QLabel('Address:')
        self.billed_to_address_input = QLineEdit()
        self.billed_to_phone_label = QLabel('Phone Number:')
        self.billed_to_phone_input = QLineEdit()
        self.billed_to_pan_label = QLabel('PAN:')
        self.billed_to_pan_input = QLineEdit()
        self.billed_to_email_label = QLabel('Email:')
        self.billed_to_email_input = QLineEdit()

        # Create widgets for Invoice Details
        self.invoice_number_label = QLabel('Invoice Number:')
        self.invoice_number_input = QLineEdit()

        self.invoice_date_label = QLabel('Invoice Date:')
        self.invoice_date_input = QDateEdit()
        # Set default date to current date
        self.invoice_date_input.setDate(QDate.currentDate())

        self.due_date_label = QLabel('Due Date:')
        self.due_date_input = QDateEdit()
        # Set default date to current date
        self.due_date_input.setDate(QDate.currentDate())

        # Create widgets for Item Details Table
        self.items_table = QTableWidget()
        # Updated column count to include checkbox
        self.items_table.setColumnCount(10)
        self.items_table.setHorizontalHeaderLabels([
            "", 'Name', 'Description', 'HSN Code', 'Quantity',
            'Unit Price', 'GST(%)', 'SGST (%)', 'CGST (%)', 'Total'
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

        # Create header checkbox for bulk selection
        self.select_all_checkbox = QCheckBox()
        self.select_all_checkbox.setToolTip('Select/Deselect All')
        self.items_table.setHorizontalHeaderItem(0, QTableWidgetItem())
        self.items_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.setCellWidget(0, 0, self.select_all_checkbox)
        self.select_all_checkbox.stateChanged.connect(self.select_all_items)

        self.items_table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)

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

        # drop dwon
        self.billed_by_dropdown_label = QLabel('Select Billed By:')
        self.billed_by_dropdown = QComboBox()
        self.billed_by_dropdown.activated.connect(self.populate_billed_by_fields)
        #self.billed_by_dropdown.currentIndexChanged.connect(self.populate_billed_by_fields)

        # Create widgets for Billed To dropdown
        self.billed_to_dropdown_label = QLabel('Select Billed To:')
        self.billed_to_dropdown = QComboBox()
        self.billed_to_dropdown.activated.connect(self.populate_billed_to_fields)
        #self.billed_to_dropdown.currentIndexChanged.connect(self.populate_billed_to_fields)

        # Create layouts for sections
        billed_by_form = QFormLayout()
        billed_by_form.addRow(self.billed_by_cname_label,self.billed_by_cname_input)
        billed_by_form.addRow(self.billed_by_gst_label,
                              self.billed_by_gst_input)
        billed_by_form.addRow(self.billed_by_address_label,
                              self.billed_by_address_input)
        billed_by_form.addRow(self.billed_by_phone_label,
                              self.billed_by_phone_input)
        billed_by_form.addRow(self.billed_by_pan_label, self.billed_by_pan_input)
        billed_by_form.addRow(self.billed_by_email_label, self.billed_by_email_input)
        

        billed_to_form = QFormLayout()
        billed_to_form.addRow(self.billed_to_cname_label, self.billed_to_cname_input)
        billed_to_form.addRow(self.billed_to_gst_label,
                              self.billed_to_gst_input)
        billed_to_form.addRow(self.billed_to_address_label,
                              self.billed_to_address_input)
        billed_to_form.addRow(self.billed_to_phone_label,
                              self.billed_to_phone_input)
        billed_to_form.addRow(self.billed_to_pan_label, self.billed_to_pan_input)
        billed_to_form.addRow(self.billed_to_email_label, self.billed_to_email_input)
        

        invoice_form = QFormLayout()
        invoice_form.addRow(self.invoice_number_label,
                            self.invoice_number_input)
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
        # Add button below items table
        main_layout.addWidget(self.add_item_button)
        main_layout.addWidget(self.total_amount_label)

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

        # Add Billers menu with sub-options
        billers_menu = QMenu('Billers', self)
        self.billers_info_action = QAction('Biller Info', self)
        self.billers_info_action.triggered.connect(self.show_biller_info_dialog)
        self.customer_info_action = QAction('Customer Info', self)
        self.customer_info_action.triggered.connect(self.show_customer_info_dialog)
        billers_menu.addAction(self.billers_info_action)
        billers_menu.addAction(self.customer_info_action)
        self.menu_bar.addMenu(billers_menu)

        # Set main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply Meta-like color scheme
        self.setStyleSheet(STYLESHEET)

        
        billed_by_form.addRow(self.billed_by_dropdown_label, self.billed_by_dropdown)
        billed_to_form.addRow(self.billed_to_dropdown_label, self.billed_to_dropdown)
        


        # Connect button signals
        self.add_item_button.clicked.connect(self.open_add_item_dialog)
        self.delete_item_button.clicked.connect(self.delete_selected_items)
        self.submit_button.clicked.connect(self.submit_invoice)
        self.print_button.clicked.connect(self.print_invoice)
        self.export_pdf_button.clicked.connect(self.export_to_pdf)
        self.update_total_amount()

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
            self.update_total_amount()

    def add_item_to_table(self, item_data):
        row_position = self.items_table.rowCount()
        self.items_table.insertRow(row_position)

        # Add checkbox in the first column for selection
        checkbox = QCheckBox()
        self.items_table.setCellWidget(row_position, 0, checkbox)

        # Add other item data
        self.items_table.setItem(
            row_position, 1, QTableWidgetItem(item_data['name']))
        self.items_table.setItem(
            row_position, 2, QTableWidgetItem(item_data['description']))
        self.items_table.setItem(
            row_position, 3, QTableWidgetItem(item_data['hsn_code']))
        self.items_table.setItem(
            row_position, 4, QTableWidgetItem(str(item_data['quantity'])))
        self.items_table.setItem(
            row_position, 5, QTableWidgetItem(str(item_data['unit_price'])))
        self.items_table.setItem(
            row_position, 6, QTableWidgetItem(str(item_data['gst'])))
        self.items_table.setItem(
            row_position, 7, QTableWidgetItem(str(item_data['sgst'])))
        self.items_table.setItem(
            row_position, 8, QTableWidgetItem(str(item_data['cgst'])))
        self.items_table.setItem(
            row_position, 9, QTableWidgetItem(str(item_data['total'])))

    def delete_selected_items(self):
        selected_rows = []
        for row in range(self.items_table.rowCount()):
            checkbox = self.items_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                selected_rows.append(row)

        # Delete rows in reverse to avoid index issues
        for row in reversed(selected_rows):
            self.items_table.removeRow(row)
        self.update_total_amount()

    def update_total_amount(self):
        """Update the total amount based on the values in the table."""
        total = 0
        for row in range(self.items_table.rowCount()):
            item_total = self.items_table.item(row, 9)
            if item_total:
                try:
                    total += float(item_total.text())
                except ValueError:
                    pass
        self.total_amount_label.setText(f'<b>Total Amount:</b> ${total:.2f}')

    def submit_invoice(self):
        invoice_holder = {}
        invoice_holder["billed_by_gst"] = self.billed_by_gst_input.text()
        invoice_holder["billed_by_address"] = self.billed_by_address_input.text()
        invoice_holder["billed_by_phone"] = self.billed_by_phone_input.text()
        invoice_holder["billed_to_gst"] = self.billed_to_gst_input.text()
        invoice_holder["billed_to_address"] = self.billed_to_address_input.text()
        invoice_holder["billed_to_phone"] = self.billed_to_phone_input.text()
        invoice_holder["invoice_number"] = self.invoice_number_input.text()
        invoice_holder["invoice_date"] = self.invoice_date_input.date().toString(
            "yyyy-MM-dd")
        invoice_holder["due_date"] = self.due_date_input.date().toString(
            "yyyy-MM-dd")
        invoice_holder["Total bill"] = self.total_amount_label.text().split("$")[-1]
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
        
        self.file_ops(invoice_holder)        
        RequestManager().post(endpoint="insert-invoices/", json=invoice_holder)
        QMessageBox.information(
            self, "Submit", "Invoice submitted successfully!")

    def print_invoice(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            self.render(painter)
            painter.end()

    def export_to_pdf(self):
        file_dialog = QFileDialog(
            self, 'Export to PDF', '', 'PDF Files (*.pdf)')
        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)

            print_dialog = QPrintDialog(printer, self)
            if print_dialog.exec() == QDialog.DialogCode.Accepted:
                painter = QPainter(printer)
                self.render(painter)
                painter.end()

    def show_invoice_list_dialog(self):
        dialog = InvoiceListDialog(self)
        dialog.exec()

    def show_biller_info_dialog(self):
        dialog = BillerInfoDialog(self)
        dialog.exec()

    def show_customer_info_dialog(self):
        dialog = CustomerInfoDialog(self)
        dialog.exec()

    def populate_billed_by_fields(self):
        selected_item = self.billed_by_dropdown.currentText()
        if selected_item:
            # Fetch and populate the selected billed by information
            data = self.fetch_billed_by_details(selected_item)
            self.billed_by_cname_input.setText(data['Company_name'])
            self.billed_by_gst_input.setText(data['GST'])
            self.billed_by_address_input.setText(data['address'])
            self.billed_by_phone_input.setText(data['phone'])
            self.billed_by_pan_input.setText(data['PAN'])
            self.billed_by_email_input.setText(data['email'])

    def populate_billed_to_fields(self):
        selected_item = self.billed_to_dropdown.currentText()
        if selected_item:
            # Fetch and populate the selected billed to information
            data = self.fetch_billed_to_details(selected_item)
            self.billed_to_cname_input.setText(data['Company_name'])
            self.billed_to_gst_input.setText(data['GST'])
            self.billed_to_address_input.setText(data['address'])
            self.billed_to_phone_input.setText(data['phone'])
            self.billed_to_pan_input.setText(data['PAN'])
            self.billed_to_email_input.setText(data['email'])


    def populate_dropdowns(self):
        # Example data fetching methods (to be implemented)
        billed_by_data = self.fetch_billed_by_data()
        billed_to_data = self.fetch_billed_to_data()

        self.billed_by_dropdown.addItems(billed_by_data)
        self.billed_to_dropdown.addItems(billed_to_data)
    
    def fetch_billed_by_data(self):
        response_data = RequestManager().get(endpoint="company-info/")
        self.biller_info = response_data.json()
        return [item["Company_name"] for item in self.biller_info]
            

    def fetch_billed_to_data(self):

        self.customer_info = RequestManager().get(endpoint="customer-company-info/").json()
        return [item["Company_name"] for item in self.customer_info]

    def fetch_billed_by_details(self, company_name):
        # Fetch details for the selected billed by entity
        # Example: {'company_name': 'Company A', 'gst': 'GST123', ...}
        for item in self.biller_info:
            if item['Company_name'] == company_name:
                return item
        return {}

    def fetch_billed_to_details(self, customer_name):
        # Fetch details for the selected billed to entity
        # Example: {'company_name': 'Customer X', 'gst': 'GST456', ...}
        for item in self.customer_info:
            if item['Company_name'] == customer_name:
                return item
        return {}




# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    if login_page.exec() == QDialog.DialogCode.Accepted:
        window = InvoicePage()
        window.resize(800, 600)
        window.show()
        sys.exit(app.exec())
