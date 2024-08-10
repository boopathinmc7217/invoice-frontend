from PyQt6.QtWidgets import QLineEdit, QFormLayout, QLabel, QDialog, QDialogButtonBox


class ItemDialog(QDialog):
    def __init__(self, parent=None) -> None:
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

        self.item_gst_label = QLabel('GST (%):')
        self.item_gst_input = QLineEdit()

        self.item_sgst_label = QLabel('SGST (%):')
        self.item_sgst_input = QLineEdit()
        self.item_sgst_input.setReadOnly(True)

        self.item_cgst_label = QLabel('CGST (%):')
        self.item_cgst_input = QLineEdit()
        self.item_cgst_input.setReadOnly(True)

        self.item_total_label = QLabel('Total:')
        self.item_total_input = QLineEdit()
        self.item_total_input.setReadOnly(True)

        # Create buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)

        # Create layout for Item Entry
        item_form = QFormLayout()
        item_form.addRow(self.item_name_label, self.item_name_input)
        item_form.addRow(self.item_description_label,
                         self.item_description_input)
        item_form.addRow(self.item_hsn_label, self.item_hsn_input)
        item_form.addRow(self.item_quantity_label, self.item_quantity_input)
        item_form.addRow(self.item_unit_price_label,
                         self.item_unit_price_input)
        item_form.addRow(self.item_gst_label, self.item_gst_input)
        item_form.addRow(self.item_sgst_label, self.item_sgst_input)
        item_form.addRow(self.item_cgst_label, self.item_cgst_input)
        item_form.addRow(self.item_total_label, self.item_total_input)
        item_form.addWidget(self.button_box)

        self.setLayout(item_form)

        # Connect signals
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.item_gst_input.textChanged.connect(self.calculate_gst_components)
        self.item_quantity_input.textChanged.connect(self.calculate_total)
        self.item_unit_price_input.textChanged.connect(self.calculate_total)
        self.item_gst_input.textChanged.connect(self.calculate_total)

    def calculate_gst_components(self):
        try:
            gst = float(self.item_gst_input.text())
            sgst = gst / 2
            cgst = gst / 2
            self.item_sgst_input.setText(f'{sgst:.2f}')
            self.item_cgst_input.setText(f'{cgst:.2f}')
        except ValueError:
            # Handle the case where the GST input is not a valid number
            self.item_sgst_input.clear()
            self.item_cgst_input.clear()

    def calculate_total(self):
        try:
            quantity = float(self.item_quantity_input.text())
            unit_price = float(self.item_unit_price_input.text())
            gst = float(self.item_gst_input.text())
            total = quantity * unit_price * (1 + gst / 100)
            self.item_total_input.setText(f'{total:.2f}')
        except ValueError:
            self.item_total_input.clear()

    def get_item_data(self) -> dict[str, str]:
        return {
            'name': self.item_name_input.text(),
            'description': self.item_description_input.text(),
            'hsn_code': self.item_hsn_input.text(),
            'quantity': self.item_quantity_input.text(),
            'unit_price': self.item_unit_price_input.text(),
            'gst': self.item_gst_input.text(),
            'sgst': self.item_sgst_input.text(),
            'cgst': self.item_cgst_input.text(),
            'total': self.item_total_input.text()
        }
