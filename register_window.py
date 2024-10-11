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
        self.username.setPlaceholderText("Логин")
        self.layout.addWidget(self.username)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password)

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться", self)
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
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректный адрес электронной почты.")
            return

        if len(username) < 4:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин должен содержать минимум 4 символа.")
            return
        
        if len(password) < 4:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 4 символа.")
            return

        if username_exists(username):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин уже существует.")
            return

        add_user(email, username, password)
        QtWidgets.QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

        self.accept()  #закрываем окно регистрации
        self.open_login_window()  #окно авторизации после регистрации

    def open_login_window(self):
        from login_window import LoginWindow  #отложенный импорт
        self.login_window = LoginWindow()
        self.login_window.exec_()  #окно авторизации

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
