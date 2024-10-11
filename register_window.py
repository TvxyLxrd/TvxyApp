from PyQt5 import QtWidgets
import re
from database import add_user, username_exists

class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 250)
        
        self.layout = QtWidgets.QVBoxLayout()

        self.email = QtWidgets.QLineEdit(self)
        self.email.setPlaceholderText("Email")
        self.layout.addWidget(self.email)

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Login")
        self.layout.addWidget(self.username)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password)

        self.register_button = QtWidgets.QPushButton("Sign In", self)
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)
        self.setStyleSheet(self.get_styles())

    def get_styles(self):
        return """
            QDialog {
                background-color: #f0f0f0;
                border-radius: 10px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def register(self):
        email = self.email.text()
        username = self.username.text()
        password = self.password.text()

        if not self.is_valid_email(email):
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a valid email address.")
            return

        if len(username) < 4:
            QtWidgets.QMessageBox.warning(self, "Error", "The login must contain at least 4 characters.")
            return
        
        if len(password) < 4:
            QtWidgets.QMessageBox.warning(self, "Error", "Password must contain at least 4 characters.")
            return

        if username_exists(username):
            QtWidgets.QMessageBox.warning(self, "Error", "Login already exists.")
            return

        add_user(email, username, password)
        QtWidgets.QMessageBox.information(self, "Success", "Registration was successful!")

        self.accept()  #closesigninwindow
        self.open_login_window()  #openauthwindowaftersignin

    def open_login_window(self):
        from login_window import LoginWindow  #deferredimport
        self.login_window = LoginWindow()
        self.login_window.exec_()  #authwindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
