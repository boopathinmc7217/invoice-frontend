from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, 
    QLabel, QMessageBox, QFormLayout, QDialog
)
from PyQt6.QtCore import Qt
import sys
import config

style_sheet = """
QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
    color: #2c3e50;
    background-color: #f4f6f9;
}

QLabel {
    color: #34495e;
    font-weight: bold;
    padding-bottom: 5px;
}

QLineEdit {
    border: 1px solid #bdc3c7;
    border-radius: 5px;
    padding: 8px;
    background-color: #ffffff;
    color: #2c3e50;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QFormLayout {
    margin: 20px;
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #ffffff;
}

QPushButton:disabled:hover {
    background-color: #bdc3c7;
}

QWidget#login_page {
    padding: 20px;
    border: 1px solid #bdc3c7;
    border-radius: 10px;
    background-color: #ffffff;
}

QLabel#login_title {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
}

QLineEdit#username_input, QLineEdit#password_input {
    margin-bottom: 10px;
}

QPushButton#login_button {
    margin-top: 10px;
}

QPushButton#forgot_password_button, QPushButton#signup_button {
    margin-top: 10px;
    color: #3498db;
}

QPushButton#forgot_password_button:hover, QPushButton#signup_button:hover {
    color: #2980b9;
}
"""

class LoginPage(QDialog):
    def __init__(self):
        super().__init__()
        self.config = config.AppConfig() 
        self.result = None  # Will be set to QDialog.DialogCode.Accepted if login is successful

        self.init_ui()
        self.setStyleSheet(style_sheet)  # Apply the stylesheet

    def init_ui(self):
        self.setWindowTitle('Login')

        # Create widgets
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setObjectName('username_input')  # Set object name for stylesheet

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hide password input
        self.password_input.setObjectName('password_input')  # Set object name for stylesheet

        self.login_button = QPushButton('Login')
        self.login_button.setObjectName('login_button')  # Set object name for stylesheet

        self.forgot_password_button = QPushButton('Forgot Password')
        self.forgot_password_button.setObjectName('forgot_password_button')  # Set object name for stylesheet

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.setObjectName('signup_button')  # Set object name for stylesheet

        # Connect signals
        self.login_button.clicked.connect(self.handle_login)
        self.forgot_password_button.clicked.connect(self.handle_forgot_password)
        self.signup_button.clicked.connect(self.handle_signup)

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow(self.username_label, self.username_input)
        form_layout.addRow(self.password_label, self.password_input)

        # Vertical layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.forgot_password_button)
        button_layout.addWidget(self.signup_button)

        # Combine form layout and button layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def handle_login(self):
        # Here you would typically validate the credentials
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            # Mock validation
            #QMessageBox.information(self, "Login", "Login successful!")
            self.result = QDialog.DialogCode.Accepted  # Set result status
            self.config.set_user_id(username)  # Store user_id
            self.accept()  # Close login window after successful login
        else:
            QMessageBox.warning(self, "Login", "Please enter both username and password.")

    def handle_forgot_password(self):
        # Handle password recovery process
        QMessageBox.information(self, "Forgot Password", "Password recovery feature not implemented.")

    def handle_signup(self):
        # Handle user signup process
        QMessageBox.information(self, "Sign Up", "Sign up feature not implemented.")

def main():
    app = QApplication(sys.argv)
    login_window = LoginPage()
    if login_window.exec() == QDialog.DialogCode.Accepted:
        # Proceed with application if login is successful
        print("Login was successful.")
    else:
        # Handle login cancellation or failure
        print("Login was not successful or cancelled.")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
