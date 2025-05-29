from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setFixedSize(400, 200)

        # Fonts
        label_font = QFont("Arial", 13, QFont.Weight.Bold)
        input_font = QFont("Arial", 15)
        button_font = QFont("Arial", 15, QFont.Weight.Bold)

        layout = QGridLayout()

        # Email Label
        self.label_email = QLabel("Email:")
        self.label_email.setFont(label_font)
        self.label_email.setStyleSheet("color: black;")

        self.email_input = QLineEdit()
        self.email_input.setFont(input_font)

        # Password Label
        self.label_password = QLabel("Password:")
        self.label_password.setFont(label_font)
        self.label_password.setStyleSheet("color: black;")

        self.password_input = QLineEdit()
        self.password_input.setFont(input_font)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(button_font)
        self.login_button.setStyleSheet(
            "background-color: #d32f2f; color: white; padding: 6px; border-radius: 5px;"
        )
        self.login_button.clicked.connect(self.validate_login)

        # Layout
        layout.addWidget(self.label_email, 0, 0)
        layout.addWidget(self.email_input, 0, 1)
        layout.addWidget(self.label_password, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.login_button, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.success = False

    def validate_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        # Dummy credentials
        if email == "admin" and password == "admin123":
            self.success = True
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
