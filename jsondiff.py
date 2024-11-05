from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QSizePolicy, QMessageBox
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt5.QtCore import Qt, QMimeData
import os
import json


class JSONDiffScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("JSON Diff")
        self.setStyleSheet("background-color: #1e1e2e; color: white;")

        # Custom font for consistency
        custom_font = QFont("Arial", 12)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header layout with Back and Diff buttons
        header_layout = QHBoxLayout()
        back_button = QPushButton("Back")
        back_button.setFont(custom_font)
        back_button.setStyleSheet(self.button_style())
        back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        back_button.clicked.connect(self.parent.show_file_select_screen)

        diff_button = QPushButton("Diff")
        diff_button.setFont(custom_font)
        diff_button.setStyleSheet(self.button_style())
        diff_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        diff_button.clicked.connect(self.show_json_diff_result_screen)

        header_layout.addWidget(back_button)
        header_layout.addStretch()
        header_layout.addWidget(diff_button)

        # File comparison section
        file_layout = QHBoxLayout()

        # File A Section
        file_a_layout = QVBoxLayout()
        file_a_label = QLabel("File A")
        file_a_label.setFont(custom_font)
        file_a_label.setAlignment(Qt.AlignCenter)
        file_a_label.setStyleSheet("font-size: 16px; color: #42aaff; background-color: #2c2f3b; padding: 4px;")

        self.file_a_drop_area = QLabel("Click to Upload JSON A...")
        self.file_a_drop_area.setStyleSheet(self.drop_area_style())
        self.file_a_drop_area.setAlignment(Qt.AlignCenter)
        self.file_a_drop_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_a_drop_area.setAcceptDrops(True)
        self.file_a_drop_area.setFixedSize(200, 200)
        self.file_a_drop_area.setFont(custom_font)
        self.file_a_drop_area.mousePressEvent = lambda event: self.open_file_dialog(self.file_a_drop_area, "A")

        file_a_layout.addWidget(file_a_label)
        file_a_layout.addWidget(self.file_a_drop_area)

        # File B Section
        file_b_layout = QVBoxLayout()
        file_b_label = QLabel("File B")
        file_b_label.setFont(custom_font)
        file_b_label.setAlignment(Qt.AlignCenter)
        file_b_label.setStyleSheet("font-size: 16px; color: #42aaff; background-color: #2c2f3b; padding: 4px;")

        self.file_b_drop_area = QLabel("Click to Upload JSON B...")
        self.file_b_drop_area.setStyleSheet(self.drop_area_style())
        self.file_b_drop_area.setAlignment(Qt.AlignCenter)
        self.file_b_drop_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_b_drop_area.setAcceptDrops(True)
        self.file_b_drop_area.setFixedSize(200, 200)
        self.file_b_drop_area.setFont(custom_font)
        self.file_b_drop_area.mousePressEvent = lambda event: self.open_file_dialog(self.file_b_drop_area, "B")

        file_b_layout.addWidget(file_b_label)
        file_b_layout.addWidget(self.file_b_drop_area)

        file_layout.addLayout(file_a_layout)
        file_layout.addLayout(file_b_layout)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(file_layout)
        self.setLayout(main_layout)

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

    def drop_area_style(self):
        return """
            QLabel {
                color: #808080;
                background-color: #3c3f41;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                border: 1px solid #2e2e2e;
            }
        """

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith(".json"):
                if event.source() == self.file_a_drop_area:
                    self.update_file_path(self.file_a_drop_area, file_path, "A")
                elif event.source() == self.file_b_drop_area:
                    self.update_file_path(self.file_b_drop_area, file_path, "B")
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a JSON file.")

    def open_file_dialog(self, drop_area, file_label):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select JSON File", "", "JSON Files (*.json)")
        if file_path:
            self.update_file_path(drop_area, file_path, file_label)

    def update_file_path(self, drop_area, file_path, file_label):
        drop_area.setText(file_path)
        if file_label == "A":
            self.parent.json_a_path = file_path
            print(f"Updated parent.json_a_path: {self.parent.json_a_path}")
        elif file_label == "B":
            self.parent.json_b_path = file_path
            print(f"Updated parent.json_b_path: {self.parent.json_b_path}")

    def show_json_diff_result_screen(self):
        if not self.parent.json_a_path or not self.parent.json_b_path:
            QMessageBox.warning(self, "Missing Files", "Please select both JSON files before proceeding.")
        else:
            self.parent.show_jsondiff_result_screen()
