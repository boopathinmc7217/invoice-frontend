from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

from request_manager import RequestManager

class CustomerInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Customer Info')

        # Layout and Widgets
        layout = QVBoxLayout()
        self.company_name_input = QLineEdit()
        self.pan_input = QLineEdit()
        self.gst_input = QLineEdit()
        self.address = QLineEdit()
        self.email = QLineEdit()
        self.phone_number = QLineEdit()
        layout.addWidget(QLabel('Company Name:'))
        layout.addWidget(self.company_name_input)
        layout.addWidget(QLabel('GST Number:'))
        layout.addWidget(self.gst_input)
        layout.addWidget(QLabel('Address:'))
        layout.addWidget(self.address)
        layout.addWidget(QLabel('Phone Number:'))
        layout.addWidget(self.phone_number)
        layout.addWidget(QLabel('PAN:'))
        layout.addWidget(self.pan_input)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)


        # Buttons
        self.save_button = QPushButton('Save')
        self.cancel_button = QPushButton('Cancel')
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)
        
        self.cancel_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.save_biller_info)

    def save_biller_info(self):
  
        data= {"Company_name":self.company_name_input.text(),
        "PAN":self.pan_input.text(),
        "GST":self.gst_input.text(),
        "address":self.address.text(),
        "email":self.email.text(),
        "phone":self.phone_number.text()}
        RequestManager().post(endpoint="customer-company-info/", json=data)
        
        self.accept()  