import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QStackedWidget
from login import LoginScreen
from signup import SignupScreen
from recoverpass import RecoverPassScreen
from fileselect import FileSelectScreen
from jsondiff import JSONDiffScreen
from jsondiff_result import JSONDiffResultScreen


def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()


class BaseApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Initialize paths as None
        self.json_a_path = ""
        self.json_b_path = ""

        # Initialize screens
        self.login_screen = LoginScreen(self)
        self.signup_screen = SignupScreen(self)
        self.recover_screen = RecoverPassScreen(self)
        self.file_select_screen = FileSelectScreen(self)
        self.json_diff_screen = JSONDiffScreen(self)
        self.json_diff_result_screen = JSONDiffResultScreen(self)
        # Add screens to the stack
        self.addWidget(self.login_screen)
        self.addWidget(self.signup_screen)
        self.addWidget(self.recover_screen)
        self.addWidget(self.file_select_screen)
        self.addWidget(self.json_diff_screen)
        self.addWidget(self.json_diff_result_screen)

        # Set the initial screen
        self.setCurrentWidget(self.login_screen)

    def show_signup_screen(self):
        self.setCurrentWidget(self.signup_screen)

    def show_login_screen(self):
        self.setCurrentWidget(self.login_screen)

    def show_recover_screen(self):
        self.setCurrentWidget(self.recover_screen)

    def show_file_select_screen(self):
        self.setCurrentWidget(self.file_select_screen)

    def show_json_diff_screen(self):
        self.setCurrentWidget(self.json_diff_screen)

    def show_jsondiff_result_screen(self):
        # Ensure JSON file paths are set in the result screen
        print("Navigating to JSON Diff Result Screen")
        if self.json_a_path and self.json_b_path:
            self.json_diff_result_screen.show_screen()  # Load content in result screen
            self.setCurrentWidget(self.json_diff_result_screen)
        else:
            print("Error: JSON file paths are not set.")


if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    main_window = BaseApp()
    main_window.show()
    sys.exit(app.exec_())
