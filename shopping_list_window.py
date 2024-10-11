from PyQt5 import QtWidgets, QtCore, QtGui

class ShoppingListWindow(QtWidgets.QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Список покупок")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout()

        # Создаем горизонтальный layout для ввода и кнопки "Добавить"
        self.input_layout = QtWidgets.QHBoxLayout()

        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setPlaceholderText("Название товара")
        self.name_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        self.input_layout.addWidget(self.name_input)

        self.quantity_input = QtWidgets.QLineEdit(self)
        self.quantity_input.setPlaceholderText("Количество")
        self.quantity_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        self.input_layout.addWidget(self.quantity_input)

        self.price_input = QtWidgets.QLineEdit(self)
        self.price_input.setPlaceholderText("Цена")
        self.price_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        self.input_layout.addWidget(self.price_input)

        # Кнопка "Добавить"
        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setIcon(QtGui.QIcon(QtGui.QPixmap('icons/add.png')))
        self.add_button.setStyleSheet("padding: 5px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.add_button.clicked.connect(self.add_item)
        self.input_layout.addWidget(self.add_button)

        self.layout.addLayout(self.input_layout)

        # Создаем QScrollArea для прокрутки списка
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9;")

        # Создаем контейнер для элементов списка
        self.items_container = QtWidgets.QWidget()
        self.items_layout = QtWidgets.QVBoxLayout(self.items_container)
        self.items_layout.setAlignment(QtCore.Qt.AlignTop)

        self.scroll_area.setWidget(self.items_container)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

        if self.user_id is None:
            self.temp_items = []  # массив для гостевого

    def add_item(self):
        name_text = self.name_input.text().strip()
        quantity_text = self.quantity_input.text().strip()
        price_text = self.price_input.text().strip()

        if name_text and quantity_text and price_text:
            item_text = f"{name_text} (Количество: {quantity_text}, Цена: {price_text})"
            self.add_item_widget(item_text)

            self.name_input.clear()
            self.quantity_input.clear()
            self.price_input.clear()

            if self.user_id is None:
                self.temp_items.append(item_text)

    def add_item_widget(self, item_text):
        item_widget = QtWidgets.QWidget()
        item_layout = QtWidgets.QHBoxLayout(item_widget)

        item_label = QtWidgets.QLabel(item_text)
        item_label.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 5px;")
        item_layout.addWidget(item_label)

        # Кнопка "Удалить"
        remove_button = QtWidgets.QPushButton(self)
        remove_button.setIcon(QtGui.QIcon(QtGui.QPixmap('icons/remove.png')))
        remove_button.setStyleSheet("padding: 5px 10px; background-color: #f44336; color: white; border: none; border-radius: 5px;")
        remove_button.clicked.connect(lambda: self.remove_item(item_widget))
        item_layout.addWidget(remove_button)

        # Кнопка "Зачеркнуть"
        cross_button = QtWidgets.QPushButton(self)
        cross_button.setIcon(QtGui.QIcon(QtGui.QPixmap('icons/mark.png')))
        cross_button.setStyleSheet("padding: 5px 10px; background-color: #ffeb3b; color: black; border: none; border-radius: 5px;")
        cross_button.clicked.connect(lambda: self.cross_item(item_label))
        item_layout.addWidget(cross_button)

        item_layout.addStretch()  # Добавляем растяжение для выравнивания кнопок справа

        # Добавляем виджет в контейнер
        self.items_layout.addWidget(item_widget)

    def remove_item(self, item_widget):
        self.items_layout.removeWidget(item_widget)
        item_widget.deleteLater()
        if self.user_id is None:
            item_text = item_widget.findChild(QtWidgets.QLabel).text()
            if item_text in self.temp_items:
                self.temp_items.remove(item_text)

    def cross_item(self, item_label):
        current_text = item_label.text()
        if "~~" not in current_text:
            item_label.setText(f"~~{current_text}~~")  # Зачеркиваем текст
            item_label.setStyleSheet("color: gray;")  # Меняем цвет текста на серый
        else:
            item_label.setText(current_text.replace("~~", ""))
            item_label.setStyleSheet("color: black;")  # Возвращаем цвет текста

    def closeEvent(self, event):
        if self.user_id is None:
            self.temp_items.clear()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ShoppingListWindow()
    window.show()
    sys.exit(app.exec_())
