from PyQt5 import QtWidgets
from database import get_user
from shopping_list_window import ShoppingListWindow
from register_window import RegisterWindow

class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 250)
        
        self.layout = QtWidgets.QVBoxLayout()
        
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Логин")
        self.layout.addWidget(self.username)

        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password)

        self.login_button = QtWidgets.QPushButton("Войти", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.register_button = QtWidgets.QPushButton("Регистрация", self)
        self.register_button.clicked.connect(self.open_register_window)
        self.layout.addWidget(self.register_button)

        self.guest_button = QtWidgets.QPushButton("Гостевой режим", self)
        self.guest_button.clicked.connect(self.guest_mode)
        self.layout.addWidget(self.guest_button)

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
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
            QPushButton:pressed {
                background-color: #449d44;
            }
        """

    def login(self):
        username = self.username.text()
        password = self.password.text()
        user = get_user(username, password)

        if user:
            self.accept()
            self.shopping_list_window = ShoppingListWindow(user_id=user[0])
            self.shopping_list_window.show()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")

    def open_register_window(self):
        self.reject()  # Закрываем текущее окно авторизации
        self.register_window = RegisterWindow()
        self.register_window.exec_()  # Открываем окно регистрации

    def guest_mode(self):
        self.accept()
        self.shopping_list_window = ShoppingListWindow(user_id=None)  # Гостевой режим
        self.shopping_list_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
