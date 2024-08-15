from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

class InvoicePreviewDialog(QDialog):
    def __init__(self, invoice_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Invoice Preview')
        self.setGeometry(100, 100, 800, 600)
        
        # Create text browser widget to display HTML content
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # Allow external links in HTML
        
        # Set the HTML content
        html_content = self.generate_html(invoice_data)
        self.text_browser.setHtml(html_content)
        
        # Create print button
        self.print_button = QPushButton('Print / Save as PDF')
        self.print_button.clicked.connect(self.show_print_save_dialog)
        
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        layout.addWidget(self.print_button)
        
        self.setLayout(layout)
    
    def generate_html(self, invoice_data):
        html_template = """
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .invoice {{ width: 100%; }}
                .header {{ text-align: center; }}
                .details {{ margin: 20px; }}
                .footer {{ margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Invoice</h1>
            </div>
            <div class="details">
                <p><strong>Invoice Number:</strong> {invoice_number}</p>
                <p><strong>Issued Date:</strong> {issued_date}</p>
                <p><strong>Billed To:</strong> {billed_to}</p>
                <p><strong>Due Date:</strong> {due_date}</p>
                <p><strong>Total Amount:</strong> {total_amount}</p>
            </div>
            <div class="footer">
                <p>Thank you for your business!</p>
            </div>
        </body>
        </html>
        """
        
        # Fill the template with data
        return html_template.format(
            invoice_number=invoice_data.get("Invoice Number", ""),
            issued_date=invoice_data.get("Issued Date", ""),
            billed_to=invoice_data.get("Billed To", ""),
            due_date=invoice_data.get("Due Date", ""),
            total_amount=invoice_data.get("Total Amount", "")
        )

    def show_print_save_dialog(self):
        # Create a custom message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Print or Save as PDF")
        msg_box.setText("Choose an option:")
        
        # Add custom buttons
        print_button = msg_box.addButton("Print", QMessageBox.ButtonRole.AcceptRole)
        pdf_button = msg_box.addButton("Save as PDF", QMessageBox.ButtonRole.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.StandardButton.Cancel)
        
        # Show the message box and wait for user input
        msg_box.exec()

        if msg_box.clickedButton() == print_button:
            self.print_invoice()
        elif msg_box.clickedButton() == pdf_button:
            self.save_as_pdf()

    def print_invoice(self):
        printer = QPrinter()

        # Create a print dialog
        print_dialog = QPrintDialog(printer, self)
        
        # Check if the user accepts the print dialog
        if print_dialog.exec() == QDialog.DialogCode.Accepted:
            # Print the invoice
            self.text_browser.print(printer)

    def save_as_pdf(self):
        printer = QPrinter()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Invoice as PDF", "", "PDF Files (*.pdf)")
        if save_path:
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(save_path)
            self.text_browser.print(printer)
