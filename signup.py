import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SignupScreen(QWidget):
    """
        Description: Sign Up Screen for Users
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Sign Up")
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Custom font
        custom_font = QFont("Arial", 12)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title_label = QLabel("Sign Up")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #42aaff;")
        title_label.setAlignment(Qt.AlignCenter)

        # Username and Password inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(custom_font)
        self.username_input.setStyleSheet(self.input_style())

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(custom_font)
        self.password_input.setStyleSheet(self.input_style())
        self.password_input.setEchoMode(QLineEdit.Password)

        # Buttons
        signup_button = QPushButton("Sign Up")
        continue_button = QPushButton("Continue to Login")
        back_button = QPushButton("Back")  # New Back button

        # Set style for buttons
        for button in [signup_button, continue_button, back_button]:
            button.setFont(custom_font)
            button.setStyleSheet(self.button_style())
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setMinimumHeight(40)

        # Connect buttons
        signup_button.clicked.connect(self.save_user)
        continue_button.clicked.connect(self.parent.show_login_screen)
        back_button.clicked.connect(self.parent.show_login_screen)  # Connect Back button to go back to login

        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(signup_button)
        layout.addWidget(continue_button)
        layout.addWidget(back_button)  # Add Back button to layout at the bottom

        self.setLayout(layout)

    def save_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", "Account created successfully")
            self.parent.show_login_screen()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists")
        conn.close()

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

    def input_style(self):
        return """
            QLineEdit {
                color: #808080;
                background-color: #3c3f41;
                padding: 10px;
                border-radius: 8px;
            }
        """
