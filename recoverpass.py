from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class RecoverPassScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Recover Password")
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Custom font
        custom_font = QFont("Arial", 12)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("Recover Password")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #42aaff;")
        title_label.setAlignment(Qt.AlignCenter)

        # Email input for recovery
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setFont(custom_font)

        # Buttons
        recover_button = QPushButton("Recover Password")
        back_button = QPushButton("Back to Login")
        for button in [recover_button, back_button]:
            button.setFont(custom_font)
            button.setStyleSheet(self.button_style())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(40)

        # Connect buttons
        recover_button.clicked.connect(self.recover_password)
        back_button.clicked.connect(self.parent.show_login_screen)

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.email_input)
        layout.addWidget(recover_button)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def recover_password(self):
        email = self.email_input.text()
        QMessageBox.information(self, "Recover Password", f"Instructions sent to {email}.")

    def button_style(self):
        return """
            QPushButton {
                color: #ffffff;
                background-color: #42aaff;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #338ccc;
            }
        """
