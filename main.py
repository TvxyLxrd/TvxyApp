from PyQt5 import QtWidgets
from login_window import LoginWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    login_window = LoginWindow()
    if login_window.exec_() == QtWidgets.QDialog.Accepted:
        pass

    sys.exit(app.exec_())
