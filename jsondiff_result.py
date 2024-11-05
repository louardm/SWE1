from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QSizePolicy, QScrollArea, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
from json_result_save import save_json_diff_to_doc  # Import the function

class JSONDiffResultScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("JSON Diff Result")
        self.setStyleSheet("background-color: #1e1e2e; color: white;")
        self.saved = False  # Track if the work is saved

        # Custom font for consistency
        custom_font = QFont("Arial", 12)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header layout with Back and Save buttons
        header_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setFont(custom_font)
        back_button.setStyleSheet(self.button_style())
        back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Fixed vertical expansion
        back_button.clicked.connect(self.check_unsaved_work)  # Connect to new function to check for unsaved work

        save_button = QPushButton("Save")
        save_button.setFont(custom_font)
        save_button.setStyleSheet(self.button_style())
        save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Fixed vertical expansion
        save_button.clicked.connect(self.save_diff_to_doc)  # Connect to save function

        header_layout.addWidget(back_button)
        header_layout.addWidget(save_button)

        # JSON content layout
        content_layout = QHBoxLayout()

        # JSON A content section with scroll
        file_a_layout = QVBoxLayout()
        file_a_label = QLabel("File A Content")
        file_a_label.setFont(custom_font)
        file_a_label.setAlignment(Qt.AlignCenter)
        file_a_label.setStyleSheet("font-size: 16px; color: #42aaff; background-color: #2c2f3b; padding: 4px;")

        json_a_scroll_area = QScrollArea()
        json_a_scroll_area.setWidgetResizable(True)
        self.json_a_content = QTextEdit()
        self.json_a_content.setStyleSheet("background-color: #3c3f41; color: white;")
        self.json_a_content.setFont(custom_font)
        self.json_a_content.setReadOnly(True)
        json_a_scroll_area.setWidget(self.json_a_content)

        file_a_layout.addWidget(file_a_label)
        file_a_layout.addWidget(json_a_scroll_area)

        # JSON B content section with scroll
        file_b_layout = QVBoxLayout()
        file_b_label = QLabel("File B Content")
        file_b_label.setFont(custom_font)
        file_b_label.setAlignment(Qt.AlignCenter)
        file_b_label.setStyleSheet("font-size: 16px; color: #42aaff; background-color: #2c2f3b; padding: 4px;")

        json_b_scroll_area = QScrollArea()
        json_b_scroll_area.setWidgetResizable(True)
        self.json_b_content = QTextEdit()
        self.json_b_content.setStyleSheet("background-color: #3c3f41; color: white;")
        self.json_b_content.setFont(custom_font)
        self.json_b_content.setReadOnly(True)
        json_b_scroll_area.setWidget(self.json_b_content)

        file_b_layout.addWidget(file_b_label)
        file_b_layout.addWidget(json_b_scroll_area)

        # Add file layouts to content layout with stretch factors
        content_layout.addLayout(file_a_layout, 1)  # Stretchable
        content_layout.addLayout(file_b_layout, 1)  # Stretchable

        # Add layouts to main layout
        main_layout.addLayout(header_layout)  # No stretch
        main_layout.addLayout(content_layout, 1)  # Stretchable

        self.setLayout(main_layout)

        # Full screen mode
        self.showFullScreen()

    def show_screen(self):
        """Method to load content each time the screen is shown."""
        self.load_content()

    def load_content(self):
        print(f"Loading content for File A: {self.parent.json_a_path}")
        self.json_a_content.setPlainText(self.load_json_content(self.parent.json_a_path))

        print(f"Loading content for File B: {self.parent.json_b_path}")
        self.json_b_content.setPlainText(self.load_json_content(self.parent.json_b_path))

    def load_json_content(self, filepath):
        print(f"Attempting to load JSON from: {filepath}")
        try:
            with open(filepath, 'r') as file:
                json_content = json.load(file)
                print(f"Successfully loaded JSON from: {filepath}")
                return json.dumps(json_content, indent=4)
        except Exception as e:
            print(f"Error loading JSON content from {filepath}: {e}")
            return f"Error loading JSON content: {e}"

    def save_diff_to_doc(self):
        # Call the save function and check the result
        output_path = "json_differences.doc"
        result = save_json_diff_to_doc(self.parent.json_a_path, self.parent.json_b_path, output_path)

        if result:
            QMessageBox.information(self, "Save Successful", f"Differences saved to {output_path}")
            self.saved = True  # Mark as saved
        else:
            QMessageBox.information(self, "No Differences", "No differences to save.")

    def check_unsaved_work(self):
        # If work is unsaved, prompt the user
        if not self.saved:
            reply = QMessageBox.question(self, "Unsaved Work",
                                         "You have unsaved work. Are you sure you want to go back?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.parent.show_json_diff_screen()
        else:
            self.parent.show_json_diff_screen()

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
