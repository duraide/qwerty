from PyQt5 import QtWidgets, uic
import sys
import random
import sqlite3
from PyQt5.QtGui import QPainter, QColor
from PyQt6.uic.properties import QtGui


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.form = None
        uic.loadUi('WQW.ui', self)
        self.pushButton.clicked.connect(self.draw_circle)
        self.addEditButton.clicked.connect(self.open_add_edit_form)
        self.conn = sqlite3.connect('coffee.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS coffee
                          (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL)''')
        self.conn.commit()
    def draw_circle(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for _ in range(5):
            diameter = random.randint(20, 100)
            x = random.randint(0, self.width() - diameter)
            y = random.randint(0, self.height() - diameter)
            painter.setBrush(QColor(random.randint(0, 255)))

            painter.drawEllipse(x, y, diameter, diameter)


    def open_add_edit_form(self):
        self.form = AddEditCoffeeForm(self.conn)
        self.form.show()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, conn):
        super(AddEditCoffeeForm, self).__init__()
        uic.loadUi('fqfq.ui', self)
        self.conn = conn
        self.saveButton.clicked.connect(self.save_coffee)

    def save_coffee(self):
        name = self.nameLineEdit.text()
        description = self.descriptionTextEdit.toPlainText()
        try:
            price = float(self.priceLineEdit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректную цену.")
            return
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO coffee (name, description, price) VALUES (?, ?, ?)',
                       (name, description, price))
        self.conn.commit()
        self.close()

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())