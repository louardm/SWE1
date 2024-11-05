import sqlite3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt


class LoginScreen(QWidget):
    """
    Description: Log in Screen for Users
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("FileComp")
        self.setFixedSize(600, 400)  # Set a fixed size for consistent design

        # Set a background color or image
        self.setStyleSheet("background-color: #1e1e2e;")  # Dark blue background

        # Custom font
        custom_font = QFont("Arial", 12)

        # Title Label
        title_label = QLabel("FileComp")
        title_label.setStyleSheet("color: #42aaff; font-size: 28px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)

        # Subtitle/Tagline
        subtitle_label = QLabel("A visually appealing and fully functional file comparison tool.")
        subtitle_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        subtitle_label.setAlignment(Qt.AlignCenter)

        # Username and Password inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(custom_font)
        self.username_input.setStyleSheet(self.input_style())

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(custom_font)
        self.password_input.setStyleSheet(self.input_style())

        # Login Button
        login_button = QPushButton("Enter")
        login_button.setFont(custom_font)
        login_button.setStyleSheet(self.button_style())
        login_button.clicked.connect(self.verify_login)

        # Sign Up Button
        signup_button = QPushButton("Sign up")
        signup_button.setFont(custom_font)
        signup_button.setStyleSheet(self.button_style())  # Apply the same style as Enter
        signup_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        signup_button.setMinimumHeight(40)
        signup_button.clicked.connect(self.parent.show_signup_screen)  # Navigate to Sign Up screen

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Spacer for spacing
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(signup_button)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(subtitle_label)

        self.setLayout(layout)

    def input_style(self):
        return """
            QLineEdit {
                color: #ffffff;
                background-color: #3c3f41;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #2e2e2e;
            }
            QLineEdit:hover {
                border: 1px solid #42aaff;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                color: #ffffff;
                background-color: #42aaff;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #338ccc;
            }
        """

    def verify_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.parent.show_file_select_screen()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
