from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


def button_style():
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


class FileSelectScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("File Selection")
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Set larger initial size
        self.setGeometry(100, 100, 800, 600)  # Initial position (x, y) and size (width, height)

        # Custom font for labels and buttons
        custom_font = QFont("Arial", 12)

        # Title label
        title_label = QLabel("Select File Type")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #42aaff;")

        # Back button that spans the width
        back_button = QPushButton("Back")
        back_button.setFont(custom_font)
        back_button.setStyleSheet(button_style())
        back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expands horizontally, fixed vertically
        back_button.setMinimumHeight(50)  # Adjust button height as needed
        back_button.clicked.connect(self.parent.show_login_screen)  # Replace with the correct method

        # File type buttons
        json_button = QPushButton("JSON")
        py_button = QPushButton("PY")
        doc_button = QPushButton("DOC")

        # Set font and size policy for each file type button
        for button in [json_button, py_button, doc_button]:
            button.setFont(custom_font)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setMinimumHeight(50)
            button.setStyleSheet(button_style())

        # Connect buttons to their respective screens
        json_button.clicked.connect(self.parent.show_json_diff_screen)
        # Placeholder for future screens:
        # py_button.clicked.connect(self.parent.show_py_diff_screen)
        # doc_button.clicked.connect(self.parent.show_doc_diff_screen)

        # Layout for file type buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(title_label)
        button_layout.addWidget(json_button)
        button_layout.addWidget(py_button)
        button_layout.addWidget(doc_button)
        button_layout.setAlignment(Qt.AlignCenter)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(back_button)  # Back button at the top spanning the width
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
